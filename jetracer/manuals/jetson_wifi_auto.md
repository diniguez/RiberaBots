
# 🚗 NVIDIA Jetson – Conexión Wi-Fi automática sin teclado

## ❌ Problema

El NVIDIA Jetson **no se conecta automáticamente a la Wi-Fi al arrancar** si no se inicia sesión con el usuario `jetson`.

Esto obliga a:
- Conectar un teclado al coche
- Iniciar sesión manualmente
- Introducir la contraseña de la Wi-Fi

### 📌 Causa
La red Wi-Fi está configurada como **conexión de usuario**, no como **conexión del sistema**.  
NetworkManager solo la activa después del login.

---

## ✅ Solución recomendada (modo coche / headless)

Configurar la Wi-Fi como **conexión global del sistema**, para que:
- Se conecte automáticamente al arrancar
- No dependa de ningún usuario
- No necesite teclado ni pantalla

---

## 1️⃣ Listar conexiones Wi-Fi existentes

```bash
nmcli connection show
```

Ejemplo de salida:
```
MiWifiCasa
```

Anota el nombre exacto de la conexión.

---

## 2️⃣ Convertir la Wi-Fi en conexión del sistema

Elimina la asociación con el usuario `jetson`:

```bash
sudo nmcli connection modify "MiWifiCasa" connection.permissions ""
```

> ⚠️ Importante:  
> `""` (vacío) indica que la conexión es **global**.

---

## 3️⃣ Activar autoconexión al arrancar

```bash
sudo nmcli connection modify "MiWifiCasa" connection.autoconnect yes
```

---

## 4️⃣ Reiniciar NetworkManager

```bash
sudo systemctl restart NetworkManager
```

---

## 5️⃣ Reiniciar el Jetson

```bash
sudo reboot
```

🚗 A partir de ahora, el Jetson se conectará a la Wi-Fi **automáticamente al arrancar**, sin login.

---

## 🧪 Verificación (opcional)

Después de arrancar sin teclado:

```bash
nmcli device status
```

Salida esperada:
```
wlan0  wifi  connected  MiWifiCasa
```

---

## 🔁 Alternativa: crear la Wi-Fi como root (desde cero)

Si prefieres borrar la conexión y crearla correctamente:

```bash
sudo nmcli dev wifi connect "MiWifiCasa" password "TU_PASSWORD"
```

Esto crea automáticamente:
- Conexión global
- Autoconexión activa
- Independiente de usuarios

---

## ⚡ Optimización recomendada para uso en coche

Evita retrasos en el arranque si no hay red disponible:

```bash
sudo systemctl disable NetworkManager-wait-online.service
```

---

## 🚀 Opcionales avanzados

- 🔑 Acceso SSH automático
- 📡 Hotspot automático si no hay Wi-Fi
- 🔄 Reconexión en movimiento
- 🔋 Optimización de consumo energético

---

## ℹ️ Notas

- Compatible con Jetson Nano, Xavier, Orin
- Basado en Ubuntu / L4T con NetworkManager
- Ideal para sistemas embebidos y headless

---
