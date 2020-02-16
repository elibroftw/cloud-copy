import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart';

// const BASE_URL = 'http://167.99.191.206/';
const BASE_URL = 'http://127.0.0.1:5000/';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
      // This widget is the root of your application.
      @override
      Widget build(BuildContext context) {
        return MaterialApp(
          title: 'Flutter login UI',
          theme: ThemeData(
            // This is the theme of your application.
            //
            // Try running your application with "flutter run". You'll see the
            // application has a blue toolbar. Then, without quitting the app, try
            // changing the primarySwatch below to Colors.green and then invoke
            // "hot reload" (press "r" in the console where you ran "flutter run",
            // or simply save your changes to "hot reload" in a Flutter IDE).
            // Notice that the counter didn't reset back to zero; the application
            // is not restarted.
            primarySwatch: Colors.blue,
          ),
          home: MyHomePage(title: 'Flutter Login'),
        );
      }
    }

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}



class _MyHomePageState extends State<MyHomePage> {
      TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20.0);
      TextEditingController emailController = new TextEditingController();
      TextEditingController passwordController = new TextEditingController();

//      postReq(String email, String password) async {
//      }
      _loginPressed() async {
        String email = emailController.text;
        String password = passwordController.text;
        if (email == "" || password == "") {
          print("All fields must be completed");
        } else {
          final client = HttpClient();
          final request = await client.post(BASE_URL, 5000, "authenticate/");
          request.headers.set(HttpHeaders.contentTypeHeader, "plain/text"); // or headers.add()
          request.write('{"email": "$email", "password": "$password"}');
          final response = await request.close();
          final body = response.toString();
//          String url = BASE_URL + "authenticate/";
//          Map<String, String> headers = {"Content-type": "application/json"};
//          String json = '{"email": "$email", "password": "$password"}';
//          Response response = await post(url, headers: headers, body: json);
//          String body = response.body;
          response.transform(utf8.decoder).listen((contents) {
            print(contents);
          });
          // check if body is false, else its a token
        }
      }

      @override
      Widget build(BuildContext context) {

        final emailField = TextField(
          controller: emailController,
          obscureText: false,
          style: new TextStyle(color: Colors.white),
          decoration: InputDecoration(
              contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
              hintText: "Email",
              hintStyle: TextStyle(fontSize: 20.0, color: Colors.blueGrey),
              border:
                  OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))),
        );
        final passwordField = TextField(
          controller: passwordController,
          obscureText: true,
          style: new TextStyle(color: Colors.white),
          decoration: InputDecoration(
              contentPadding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
              hintText: "Password",
              hintStyle: TextStyle(fontSize: 20.0, color: Colors.blueGrey),
              border:
                  OutlineInputBorder(borderRadius: BorderRadius.circular(32.0))),
        );
        final loginButon = Material(
          elevation: 5.0,
          borderRadius: BorderRadius.circular(30.0),
          color: Color(0xff01A0C7),
          child: MaterialButton(
            minWidth: MediaQuery.of(context).size.width,
            padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
            onPressed: _loginPressed,
            child: Text("Login / Sign Up",
                textAlign: TextAlign.center,
                style: style.copyWith(
                    color: Colors.white, fontWeight: FontWeight.bold)),
          ),
        );

        return Scaffold(
          resizeToAvoidBottomPadding: false,
          body: Center(
            child: Container(
              color: Colors.black,
              child: Padding(
                padding: const EdgeInsets.all(36.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    SizedBox(
                      height: 155.0,
                      child: Image.asset(
                        "assets/logo.png",
                        fit: BoxFit.contain,
                      ),
                    ),
                    SizedBox(height: 45.0),
                    emailField,
                    SizedBox(height: 25.0),
                    passwordField,
                    SizedBox(
                      height: 35.0,
                    ),
                    loginButon,
                    SizedBox(
                      height: 15.0,
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      }
    }
