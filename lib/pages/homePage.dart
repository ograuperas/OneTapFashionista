import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:hexcolor/hexcolor.dart';
import 'package:http/http.dart' as http;

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
                EdgeInsets.only(left: 100, right: 100, bottom: 50, top: 10),
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
                  width: 300,
                  height: 350,
                  color: Colors.blue,
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
