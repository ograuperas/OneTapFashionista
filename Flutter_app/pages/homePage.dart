import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'optionPage.dart';

class HomePage extends StatelessWidget {
  final String baseUrl = 'http://127.0.0.1/';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: HexColor('#75CD9B'),
        child: Center(
          child: Padding(
            padding:
                EdgeInsets.only(left: 70, right: 70, bottom: 50, top: 50),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                Text(
                  'ONE TAP FASHIONISTA',
                  style: TextStyle(
                    fontSize: 38,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
                Container(
                  //width: 300,
                  //height: 350,
                  //color: Colors.blue,
                  child: Image(
                    image: AssetImage('lib/img/home.png'),
                    fit: BoxFit.contain,
                  ),
                ),
                //Image(
                //image: NetworkImage(),
                //rounded corners

                //  ),
                SizedBox(
                  width: double.infinity, // <-- match_parent
                  height: 80,

                  child: ElevatedButton(
                    style: ButtonStyle(
                      shape: MaterialStateProperty.all<RoundedRectangleBorder>(
                        RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(5),
                        ),
                      ),
                      backgroundColor: MaterialStateProperty.all(Colors.white),
                    ),
                    onPressed: () {
                      Navigator.of(context).pushNamed(ImagePage.routeName);
                    },
                    child: Text(
                      'START NOW',
                      style: TextStyle(
                        fontSize: 30,
                        color: Colors.black,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
