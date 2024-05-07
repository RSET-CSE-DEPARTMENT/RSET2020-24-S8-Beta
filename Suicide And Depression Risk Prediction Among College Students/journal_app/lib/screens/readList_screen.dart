// ignore: file_names
// ignore_for_file: prefer_const_constructors, file_names, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:journal_app/components.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants.dart';
import 'add_entry_screen.dart';

class ReadEntryList extends StatefulWidget {
  final List<QueryDocumentSnapshot> docs;

  const ReadEntryList({
    Key? key,
    required this.docs,
  }) : super(key: key);

  @override
  State<ReadEntryList> createState() => _ReadEntryListState();
}

class _ReadEntryListState extends State<ReadEntryList> {
  String? username;
  String? classname;
  String? name;
  @override
  void initState() {
    super.initState();
     _loadSharedPrefs(); // Load the QR code image when the home page is initialized
  }
  _loadSharedPrefs() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      username = prefs.getString('username');
      classname = prefs.getString('classname');
      name = prefs.getString('name');
    });
  }
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: Container(
          width: double.infinity,
          height: double.infinity,
          decoration: kScreenBg,
          child: widget.docs.isEmpty
              ? Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      height: 20,
                    ),
                    JournyTitle(),
                    SizedBox(
                      height: 20,
                    ),
                    Expanded(
                      child: Center(
                        child: Text(
                          'Please Add Entry',
                          style: kButtonText,
                        ),
                      ),
                    ),
                    SizedBox(
                      height: 20,
                    ),
                    JournyButton(
                      label: 'Add Entry',
                      fn: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) {
                              return AddEntryScreen(username:username ,classname:classname ,);
                            },
                          ),
                        );
                      },
                    ),
                    SizedBox(
                      height: 20,
                    ),
                  ],
                )
              : Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      height: 30,
                    ),
                    JournyTitle(),
                    SizedBox(
                      height: 20,
                    ),
                    Expanded(
                      child: ListView.separated(
                        itemBuilder: (context, index) {
                          return EntryTile(
                            title: widget.docs.elementAt(index)['Title'],
                            entry: widget.docs.elementAt(index)['Entry'],
                            dateTime: widget.docs.elementAt(index)['Date'],
                          );
                        },
                        separatorBuilder: (context, index) {
                          return SizedBox(
                            height: 10,
                          );
                        },
                        itemCount: widget.docs.length,
                      ),
                    ),
                    SizedBox(
                      height: 20,
                    ),
                    JournyButton(
                        label: "BACK",
                        fn: () {
                          Navigator.pop(context);
                        }),
                    SizedBox(
                      height: 30,
                    ),
                  ],
                ),
        ),
      ),
    );
  }
}