package com.example.clipboard_1;

import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import androidx.annotation.Nullable
import androidx.core.app.NotificationCompat
import android.content.SharedPreferences
import android.content.Context
import android.content.ClipboardManager
import java.sql.Timestamp
import java.sql.Date
import java.lang.Thread
import java.security.SecureRandom
import com.android.volley.toolbox.Volley
import com.beust.klaxon.JsonObject
import javax.crypto.Mac
import javax.crypto.MacSpi
import javax.crypto.spec.SecretKeySpec
import javax.crypto.spec.PBEKeySpec

//import klaxon.JsonObject

internal class MyService:Service() {
    private val BASE_URL = "http://167.99.191.206/"
    override fun onCreate() {
        super.onCreate();
        // what is startForeground?
        val mPrefs = getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)
//        val mPrefs = this.getSharedPreferences(getString(R.string.preference_file_key), Context.MODE_PRIVATE)
//        val mPrefs = activity?.getPreferences(Context.MODE_PRIVATE)
        val email = mPrefs.getString("flutter.email", "")
        val token = mPrefs.getString("flutter.token", "")
        val cryptionKey = mPrefs.getString("flutter.cryptionKey", "")
        val queue = Volley.newRequestQueue(this)
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        var currentCopy = clipboard.getPrimaryClip().getItemAt(0).text.toString()
        var lastUpdate = Date(System.currentTimeMillis())
        println(lastUpdate) // TODO: better format
//        ClipData.newPlainText("text", et_copy_text.text);
//        myClipboard?.setPrimaryClip(myClip);
        val getNewCopyURL = "${BASE_URL}newest-copy/?token=${token}"
        val sendNewCopyURL = "${BASE_URL}share-copy/"
//        var newCopy
//        while true {
//            // TODO: try catch no internet error
//            newCopy = clipboard.getPrimaryClip().getItemAt(0).text.toString()
//            if currentCopy != newCopy {
//                // TODO: make a post request to share-copy
////                currentCopy = newCopy
//            } else {
//
//                val stringRequest = StringRequest(Request.Method.GET, getNewCopyURL,
//                        Response.Listener<String> { response ->
//                            val json: JsonObject = Parser().parse(response) as JsonObject
//                            newCopy = decrypt(key, json.get('current_copy'))
//                            var timestamp = json.get('timestamp')
//                            timestamp = Timestamp.valueOf(timestamp)
//                            Response.ErrorListener { println("That didn't work!")})
//                    queue.add(stringRequest)
//
//
//                // get request to newest-copy/?token=
//                // check if resp is not false
//                // then check if currentCopy != newCopy and
//                // if the time given > lastUpdate
//                // if false, post a notification to tell user to log in again
//            }
//            Thread.sleep(1500)
//        }
    }

    fun encrypt(key: ByteArray, text: String): String {
        // TODO
        return ""
    }

    fun decrypt(key: ByteArray, text: String): String {
        // TODO
        return ""
    }
    @Nullable
    override fun onBind(intent:Intent): IBinder? {
        return null;
    }
}