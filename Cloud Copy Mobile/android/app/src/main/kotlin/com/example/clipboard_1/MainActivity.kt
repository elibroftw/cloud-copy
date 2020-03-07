package com.example.clipboard_1;

import android.os.Build;
import android.os.Bundle;
import android.content.Intent
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import io.flutter.plugins.GeneratedPluginRegistrant

class MainActivity: FlutterActivity() {

    private var forService: Intent? = null
    private val CHANNEL = "com.cloud_copy.monitor"

//    override protected fun onCreate(savedInstanceState: Bundle) {
    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
//        super.onCreate(savedInstanceState);
        GeneratedPluginRegistrant.registerWith(flutterEngine)
        forService = Intent(this, MyService::class.java)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
                .setMethodCallHandler { call, result ->
                    if (call.method == "startService") {
                        startService()
                        result.success("Service Started")
                    }
                }
    }

    override protected fun onDestroy() {
        super.onDestroy();
        stopService(forService);
    }

    private fun startService() {
        startService(forService);
//        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
//            startForegroundService(forService);
//        } else {
//            startService(forService);
//        }
    }
}
