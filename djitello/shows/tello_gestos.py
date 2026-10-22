"""
Control del DJI RoboMaster TT (Tello Talent) mediante gestos de una mano.
Librerías: djitellopy, opencv-python, mediapipe

GESTOS (mano frente a la cámara del dron):
  Palma abierta (5 dedos), mantenida ~2.0 s -> DESPEGAR
  Puño cerrado, mantenido ~2.0 s            -> ATERRIZAR
  Índice solo                               -> SUBIR
  Índice + corazón (V)                      -> BAJAR
  Índice + corazón + anular (3 dedos)       -> ADELANTE
  4 dedos (sin pulgar)                      -> ATRÁS
  Pulgar solo                               -> DERECHA
  Meñique solo                              -> IZQUIERDA
  Pulgar + índice (L)                       -> GIRAR (horario)
  Pulgar + meñique (shaka)                  -> GIRAR (antihorario)
  Sin mano / gesto desconocido              -> STOP (hover)

TECLAS: q = aterrizar y salir | e = parada de emergencia (apaga motores)
"""
import math
import time

import cv2
import mediapipe as mp
from djitellopy import Tello

# ----------------------------- CONFIGURACIÓN -----------------------------
SPEED = 20            # velocidad RC (-100..100). Empieza bajo.
YAW_SPEED = 50        # velocidad de giro
STABLE_FRAMES = 6     # frames seguidos con el mismo gesto para aceptarlo
TAKEOFF_HOLD = 2.0    # segundos manteniendo palma abierta para despegar
LAND_HOLD = 2.0       # segundos manteniendo puño para aterrizar
SWAP_RGB = True      # pon True si los colores se ven invertidos (azul/rojo)

# Mapa gesto -> (left_right, forward_back, up_down, yaw)
# Si el movimiento izquierda/derecha te resulta invertido, cambia el signo.
MOVES = {
    "UP":       (0, 0, SPEED, 0),
    "DOWN":     (0, 0, -SPEED, 0),
    "FORWARD":  (0, SPEED, 0, 0),
    "BACK":     (0, -SPEED, 0, 0),
    "RIGHT":    (SPEED, 0, 0, 0),
    "LEFT":     (-SPEED, 0, 0, 0),
    "YAW_CW":   (0, 0, 0, YAW_SPEED),
    "YAW_CCW":  (0, 0, 0, -YAW_SPEED),
}

# --------------------------- DETECCIÓN DE GESTOS -------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


def dist(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def fingers_state(lm):
    """Devuelve [pulgar, índice, corazón, anular, meñique] (True = extendido).
    Usa distancias a la muñeca, así funciona con cualquier mano y orientación."""
    wrist = lm[0]
    state = []
    # Pulgar: la punta (4) está más lejos de la base del meñique (17) que la IP (3)
    state.append(dist(lm[4], lm[17]) > dist(lm[3], lm[17]) * 1.15)
    # Resto: punta (8,12,16,20) más lejos de la muñeca que la articulación PIP (6,10,14,18)
    for tip, pip in ((8, 6), (12, 10), (16, 14), (20, 18)):
        state.append(dist(lm[tip], wrist) > dist(lm[pip], wrist) * 1.10)
    return state


def classify(state):
    t, i, m, r, p = state
    if all(state):
        return "OPEN"
    if not any(state):
        return "FIST"
    if (not t) and i and (not m) and (not r) and (not p):
        return "UP"
    if (not t) and i and m and (not r) and (not p):
        return "DOWN"
    if (not t) and i and m and r and (not p):
        return "FORWARD"
    if (not t) and i and m and r and p:
        return "BACK"
    if t and not (i or m or r or p):
        return "RIGHT"
    if p and not (t or i or m or r):
        return "LEFT"
    if t and i and not (m or r or p):
        return "YAW_CW"
    if t and p and not (i or m or r):
        return "YAW_CCW"
    return "NONE"


# --------------------------------- MAIN ----------------------------------
def main():
    tello = Tello()
    tello.connect()
    print(f"Batería: {tello.get_battery()}%")
    tello.streamon()
    frame_read = tello.get_frame_read()

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    )

    flying = False
    last_gesture, count = "NONE", 0
    confirmed = "NONE"
    hold_start = None

    try:
        while True:
            frame = frame_read.frame
            if frame is None:
                continue
            if SWAP_RGB:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)

            gesture = "NONE"
            if res.multi_hand_landmarks:
                hand = res.multi_hand_landmarks[0]
                gesture = classify(fingers_state(hand.landmark))
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # Filtro de estabilidad: el gesto debe repetirse varios frames
            if gesture == last_gesture:
                count += 1
            else:
                last_gesture, count = gesture, 1
            if count >= STABLE_FRAMES:
                confirmed = gesture
            if gesture != confirmed and count >= STABLE_FRAMES:
                confirmed = gesture

            # ---- Acciones ----
            now = time.time()
            if confirmed in ("OPEN", "FIST"):
                # Acciones críticas: requieren mantener el gesto un tiempo
                if hold_start is None or hold_start[0] != confirmed:
                    hold_start = (confirmed, now)
                held = now - hold_start[1]
                if confirmed == "OPEN" and not flying and held >= TAKEOFF_HOLD:
                    print(">> DESPEGANDO")
                    tello.takeoff()
                    flying = True
                    hold_start = None
                elif confirmed == "FIST" and flying and held >= LAND_HOLD:
                    print(">> ATERRIZANDO")
                    tello.send_rc_control(0, 0, 0, 0)
                    tello.land()
                    flying = False
                    hold_start = None
                elif flying:
                    tello.send_rc_control(0, 0, 0, 0)
            else:
                hold_start = None
                if flying:
                    lr, fb, ud, yaw = MOVES.get(confirmed, (0, 0, 0, 0))
                    tello.send_rc_control(lr, fb, ud, yaw)

            # ---- Interfaz ----
            cv2.putText(frame, f"Gesto: {confirmed}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.putText(frame, f"{'EN VUELO' if flying else 'EN TIERRA'}  Bat:{tello.get_battery()}%",
                        (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.imshow("Tello - Gestos", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("e"):
                tello.emergency()
                flying = False
                break
    finally:
        try:
            if flying:
                tello.send_rc_control(0, 0, 0, 0)
                tello.land()
        except Exception:
            pass
        tello.streamoff()
        tello.end()
        hands.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
