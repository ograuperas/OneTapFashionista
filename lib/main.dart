import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:sm_flutter/pages/ColorPickerPage.dart';
import 'package:sm_flutter/pages/homePage.dart';
import 'package:sm_flutter/pages/optionPage.dart';
import 'package:camera/camera.dart';

Future<void> main() async {

  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  final firstCamera = cameras.first;

  runApp(MyApp(firstCamera: firstCamera,));
}

class MyApp extends StatelessWidget {
  final firstCamera;
  // This widget is the root of your application.
  MyApp({this.firstCamera});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primaryColor: HexColor('#75CD9B'),
      ),
      initialRoute: '/',
      routes: {
        '/': (ctx) => HomePage(),
        ImagePage.routeName: (ctx) => ImagePage(),
        ColorPickerPage.routeName: (ctx) => ColorPickerPage(),


      },
    );
  }
}

