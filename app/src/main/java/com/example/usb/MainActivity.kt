package com.example.usb

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import com.example.usb.ui.theme.USBTheme
import androidx.compose.foundation.gestures.awaitFirstDown

class MainActivity : ComponentActivity() {

    // Instanciamos el cliente
    private val mouseClient = MouseClient("127.0.0.1", 5000)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            USBTheme {
                var isConnected by remember { mutableStateOf(false) }

                // Intentar conectar al iniciar la pantalla
                LaunchedEffect(Unit) {
                    mouseClient.connect()
                    isConnected = true
                }

                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Box(modifier = Modifier.padding(innerPadding)) {
                        MousePadScreen(
                            mouseClient = mouseClient,
                            isConnected = isConnected
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun MousePadScreen(mouseClient: MouseClient, isConnected: Boolean) {
    var isDraggingFile by remember { mutableStateOf(false) }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(if (isDraggingFile) Color(0xFF444444) else if (isConnected) Color(0xFF1C1C1C) else Color.Red)
            .pointerInput(isConnected) {
                if (!isConnected) return@pointerInput

                awaitPointerEventScope {
                    var lastTapTime = 0L

                    while (true) {
                        val down = awaitFirstDown()
                        val currentTime = System.currentTimeMillis()
                        var hasMovedSignificantly = false // bandera

                        // Detectar inicio de Doble Toque (Arrastre)
                        if (currentTime - lastTapTime < 300) {
                            isDraggingFile = true
                            mouseClient.sendMouseDown()
                        }
                        lastTapTime = currentTime

                        while (true) {
                            val event = awaitPointerEvent()
                            val anyInProgress = event.changes.any { it.pressed }

                            if (anyInProgress) {
                                val change = event.changes.first()
                                val dragAmount = change.position - change.previousPosition

                                // Si el dedo se mueve más de 2 píxeles, marcamos que YA NO es un click
                                if (dragAmount.getDistance() > 2f) {
                                    hasMovedSignificantly = true
                                }

                                val sensitivity = 2.5f
                                mouseClient.sendMovement(
                                    (dragAmount.x * sensitivity).toInt(),
                                    (dragAmount.y * sensitivity).toInt()
                                )
                                change.consume()
                            } else {
                                // el dedo se levanta
                                if (isDraggingFile) {
                                    mouseClient.sendMouseUp()
                                    isDraggingFile = false
                                } else if (!hasMovedSignificantly) {
                                    // solo hacemos click si el dedo no se movio
                                    mouseClient.sendClick()
                                }
                                break
                            }
                        }
                    }
                }
            }
    ) {
        Text(
            text = if (isDraggingFile) "MODO ARRASTRE" else "Touchpad USB",
            color = Color.White,
            modifier = Modifier.align(Alignment.Center)
        )
    }
}