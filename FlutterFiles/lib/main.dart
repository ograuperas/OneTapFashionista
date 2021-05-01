import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _MyAppState();
  }
}

class _MyAppState extends State<MyApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Column(
          children: <Widget>[
            Text('ok1'),
            //importar imatge
            RaisedButton(//Elevated button
               child: Text('start now'),
               onPressed: null,
            ),
          ],
        ),
      ),
    );
  }
}
