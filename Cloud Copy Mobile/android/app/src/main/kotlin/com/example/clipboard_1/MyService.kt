package com.example.clipboard_1;

import android.app.IntentService
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.annotation.Nullable
import android.content.SharedPreferences
import android.content.Context
import android.content.ClipboardManager
import java.sql.Timestamp
import java.sql.Date
import java.lang.Thread
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec
import kotlin.concurrent.thread
import com.google.gson.*

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.json.JSONObject
//import io.karn


internal class MyService : IntentService("ClipboardMonitor") {
    private val baseURL = "http://167.99.191.206/"
    private val getNewCopyURL = "${baseURL}newest-copy/?token=${token}"
    private val sendNewCopyURL = "${baseURL}share-copy/"
    private lateinit var KEY: ByteArray

    override fun onHandleIntent(intent: Intent?) {
        // what is startForeground?
        startMonitoring()
//        thread(start=true, isDaemon=true) {
//            startMonitoring()
//        }
    }

    fun encrypt(text: String): ByteArray {
        val algorithm = "HmacSHA256"
        val mac = Mac.getInstance(algorithm)
        mac.init(SecretKeySpec(KEY, algorithm))
        return mac.doFinal(text.toByteArray())
    }

    fun decrypt(text: String): ByteArray {
        val algorithm = "HmacSHA256"
        val mac = Mac.getInstance(algorithm)
        mac.init(SecretKeySpec(KEY, algorithm))
        return mac.doFinal(text.toByteArray())
    }

    fun startMonitoring() {
        val mPrefs = getSharedPreferences("FlutterSharedPreferences", Context.MODE_PRIVATE)
        val email = mPrefs.getString("flutter.email", "")
        val token = mPrefs.getString("flutter.token", "")
        KEY = mPrefs.getString("flutter.key", "").toByteArray()
        val gson = Gson()
        val queue = Volley.newRequestQueue(this)
        val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager?
        var lastUpdate = Date(System.currentTimeMillis())
        println("lastUpdate = " + lastUpdate) // TODO: better format
        var currentCopy = ""
        var newCopy = ""
        // ClipData.newPlainText("text", et_copy_text.text);
        // myClipboard?.setPrimaryClip(myClip);
        while (mPrefs.getString("flutter.email", "") == email) {
            // TODO: try catch no internet error
            val temp = clipboard?.getPrimaryClip()?.getItemAt(0)?.text
            if (temp != null) newCopy = temp.toString()
            // println(newCopy)
            // https://abhiandroid.com/programming/volley
            if (newCopy != currentCopy) {
                println("send copy: ${newCopy}")
                sendCopy(newCopy)
                currentCopy = newCopy
                println("set new copy")
                val gson = Gson()
                val httpClient = HttpClientBuilder.create().build()
                val post = HttpPost(sendNewCopyURL)
                val map = HashMap<String, String>()
                map.put("token", token)
                map.put("content", encrypt(newCopy))
                post.setEntity(JSONobject(map).toString())
                post.setHeader("Content-type", "application/json")
                val response = httpClient.execute(post)
                println(response.text)
                // currentCopy = newCopy
                // val stringRequest = StringRequest(Request.Method.POST, sendNewCopyURL,
                // post(sendNewCopyURL, data=mapOf("token" to token, "contents" to encrypt(newCopy)))
            } else {
                val stringRequest = StringRequest(Request.Method.GET, getNewCopyURL,
                        Response.Listener { response ->
                            if (response != "false") {
                                val dataJSON = gson.fromJson(response, JSONObject::class.java)
                                var newCopy = dataJSON.get("contents")
                                var timestamp = dataJSON.get("timestamp")
                                println(newCopy)
                                println(timestamp)
//                                var eg = decrypt(newCopy).toString(Charsets.UTF_8)
//                                println(eg)
                                // TODO: string to Date
                                // myClipboard?.setPrimaryClip(newCopy);
                            }
                        }, Response.ErrorListener {
                    fun onErrorResponse(error: VolleyError?) {
                        // TODO: handle no internet here
                    }
                })
                // var resp = URL(getNewCopyURL).readText()
                // if resp != 'false':
                //     resp = gson.fromJson(resp, Article::class.java)  // now a map
                //     new_copy = decrypt(resp.get("current_copy")).toString()
                //     timestamp = resp.get("timestamp")
                //     if new_copy != current_text and last_update < timestamp:
                //         last_update = timestamp
                //         current_text = new_copy
                //         pyperclip.copy(new_copy)
                // get request to newest-copy/?token=
                // check if resp is not false
                // then check if currentCopy != newCopy and
                // if the time given > lastUpdate
                // if false, post a notification to tell user to log in again
            }
            Thread.sleep(1500)
        }
    }

    @Nullable
    override fun onBind(intent: Intent): IBinder? {
        return null;
    }
}