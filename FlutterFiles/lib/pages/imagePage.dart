import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:sm_flutter/pages/ColorPickerPage.dart';


class ImagePage extends StatelessWidget {
  static const routeName = '/imagePage';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: HexColor('#75CD9B'),

    body: Stack(
        children: <Widget>[
          Positioned(
            top: 0,
            left: 0,
            child: FloatingActionButton(onPressed: (){
              Navigator.of(context).pop();
            },
              elevation: 0,
              backgroundColor: HexColor('#75CD9B'),
              child: Icon(Icons.arrow_back,color: Colors.black,),
            ),
          ),
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                InkWell(
                  onTap: () {
                    // TODO https://flutter.dev/docs/cookbook/plugins/picture-using-camera
                    Navigator.of(context).pushNamed(ColorPickerPage.routeName);
                  },
                  child: Icon(
                    Icons.photo_camera,
                    size: 100,
                  ),
                ),
                Text('or'),
                InkWell(
                  onTap: () {
                    //TODO image_picker API
                    //Navigator.of(context).pushNamed(GetPage.routeName);
                  },
                  child: Icon(
                    Icons.upload_file,
                    size: 100,
                   // color: Colors.white,
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
