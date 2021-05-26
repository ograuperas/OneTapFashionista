import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:image_picker/image_picker.dart';
import 'package:sm_flutter/pages/ColorPickerPage.dart';
import 'package:camera/camera.dart';
import 'dart:io';

class ImagePage extends StatelessWidget {
  static const routeName = '/optionPage';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
      ),
      backgroundColor: HexColor('#75CD9B'),
      body: Stack(
        children: <Widget>[
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                InkWell(
                  onTap: () {
                    Navigator.of(context)
                        .pushNamed(ColorPickerPage.routeName, arguments: 1);
                  },
                  child: Icon(
                    Icons.photo_camera,
                    size: 100,
                  ),
                ),
                Text(
                  'or',
                  style: TextStyle(
                    fontSize: 25,
                  ),
                ),
                InkWell(
                  onTap: () {
                    Navigator.of(context)
                        .pushNamed(ColorPickerPage.routeName, arguments: 2);
                  },
                  child: Icon(
                    Icons.upload_file,
                    size: 100,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
