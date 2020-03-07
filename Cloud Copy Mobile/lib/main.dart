import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:password_hash/pbkdf2.dart';
import 'package:password_hash/salt.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([DeviceOrientation.portraitUp]);
  runApp(new MyApp());
}

String email;
SharedPreferences prefs;

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter login UI',
      theme: ThemeData(
        // This is the theme of your application.
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20.0);
  TextEditingController emailController = new TextEditingController();
  TextEditingController passwordController = new TextEditingController();
  final String baseURL = 'http://167.99.191.206/';
  String token;

  static startServiceInPlatform() {
    if (Platform.isAndroid) {
      const platform = const MethodChannel('com.cloud_copy.monitor');
      platform.invokeMethod("startService");
    } else {
      // iOS
      debugPrint('iOS Not implemented yet');
    }
  }

  List<int> generateKey(String password) {
    var generator = new PBKDF2();
    var salt = Salt.generateAsBase64String(0);
    var hash = generator.generateKey(password, salt, 100000, 32);
    return hash;
  }

  _loginPressed() async {
    email = emailController.text.trim();
    String password = passwordController.text;

    if (email == "") {
      debugPrint("Please enter an email address");
    }
    if (password == "") {
      debugPrint("Please enter the password");
//      TODO: focus on empty field
    } else {
      var url = baseURL + '/authenticate/';
      var response =
          await http.post(url, body: {'email': email, 'password': password});
      token = response.body;
      if (token == 'false') {
        debugPrint("incorrect email/password");
        // update text about invalid email/password
      } else {
        // Update gui to "logging in"
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => AccountPage()),
        );
        List<int> key = generateKey(password);
        prefs = await SharedPreferences.getInstance();
        prefs.setString('email', email);
        prefs.setString('token', token);
        prefs.setString('key', base64.encode(key));
        startServiceInPlatform();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final emailField = TextField(
      controller: emailController,
      obscureText: false,
      autofocus: true,
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
    final loginButton = Material(
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
                loginButton,
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

class AccountPage extends StatefulWidget {
  AccountPage({Key key, this.title}) : super(key: key);
  // TODO: on data connect option

  final String title;

  @override
  _AccountPageState createState() => _AccountPageState();
}

class _AccountPageState extends State<AccountPage> {
  TextStyle style = TextStyle(fontFamily: 'Montserrat', fontSize: 20);
  final String baseURL = 'http://167.99.191.206/';

  void logOut() {
    Navigator.pop(context);
    prefs.setString('email', "");
    prefs.setString('token', "");
    prefs.setString('key', "");
  }

  @override
  Widget build(BuildContext context) {
    final emailText = Text(
      'logged in as: $email',
      textAlign: TextAlign.left,
      style: style.copyWith(fontWeight: FontWeight.bold, color: Colors.white),
    );
    final logoutButton = Material(
      elevation: 5.0,
      borderRadius: BorderRadius.circular(30.0),
      color: Color(0xff01A0C7),
      child: MaterialButton(
        minWidth: MediaQuery.of(context).size.width,
        padding: EdgeInsets.fromLTRB(20.0, 15.0, 20.0, 15.0),
        onPressed: logOut,
        child: Text("Logout",
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
                SizedBox(height: 35.0),
                emailText,
                SizedBox(height: 20.0),
                logoutButton,
                SizedBox(height: 15.0),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
