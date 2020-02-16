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


internal class MyService:Service() {
//    private var PRIVATE_MODE = 0
    private val BASE_URL = "http://167.99.191.206/"
    override fun onCreate() {
        super.onCreate();
        // what is startForeground?
        val mPrefs = getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)
//        val mPrefs = this.getSharedPreferences(getString(R.string.preference_file_key), Context.MODE_PRIVATE)
//        val mPrefs = activity?.getPreferences(Context.MODE_PRIVATE)
        val email = mPrefs.getString("flutter.email", "")
        val token = mPrefs.getString("flutter.token", "")
        val queue = Volley.newRequestQueue(this)
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        println(clipboard.getPrimaryClip())
        var currentClip = ClipData.newPlainText("text", et_copy_text.text);
        myClipboard?.setPrimaryClip(myClip);
//        while true {
//
//        }
    }
    @Nullable
    override fun onBind(intent:Intent): IBinder? {
        return null;
    }
}