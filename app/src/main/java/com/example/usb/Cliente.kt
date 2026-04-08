package com.example.usb
import java.io.PrintWriter
import java.net.Socket
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MouseClient(val ip: String, val port: Int) {
    private var socket: Socket? = null
    private var out: PrintWriter? = null

    suspend fun connect() = withContext(Dispatchers.IO) {
        try {
            socket = Socket(ip, port)
            out = PrintWriter(socket!!.getOutputStream(), true)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }

    // FUNCIONES
    fun sendMovement(dx: Int, dy: Int) {
        Thread { out?.println("$dx,$dy") }.start()
    }

    fun sendClick() {
        Thread { out?.println("CLICK") }.start()
    }

    fun sendMouseDown() {
        Thread {
            try {
                out?.println("MOUSEDOWN")
            } catch (e: Exception) { e.printStackTrace() }
        }.start()
    }

    fun sendMouseUp() {
        Thread {
            try {
                out?.println("MOUSEUP")
            } catch (e: Exception) { e.printStackTrace() }
        }.start()
    }
}