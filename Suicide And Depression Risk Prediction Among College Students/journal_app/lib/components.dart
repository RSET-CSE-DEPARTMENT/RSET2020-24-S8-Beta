// ignore_for_file: prefer_const_literals_to_create_immutables, prefer_const_constructors, prefer_const_constructors_in_immutables, prefer_typing_uninitialized_variables

import 'package:flutter/material.dart';
import 'package:journal_app/screens/readEntry_screen.dart';
import './constants.dart';

class JournyTitle extends StatelessWidget {
  const JournyTitle({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Text(
          'Student\'s Diary',
          style: TextStyle(
            fontSize: 42,
            fontFamily: 'Pacifico',
            fontWeight: FontWeight.bold,
            foreground: Paint()
              ..style = PaintingStyle.stroke
              ..strokeWidth = 10
              ..color = Color(0xff00114f),
          ),
        ),
        Text(
          'Student\'s Diary',
          style: TextStyle(
            fontSize: 42,
            fontWeight: FontWeight.bold,
            fontFamily: 'Pacifico',
            color: Colors.white,
          ),
        ),
      ],
    );
  }
}

class JournyButton extends StatelessWidget {
  final String label;
  final fn;
  JournyButton({
    super.key,
    required this.label,
    required this.fn,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: fn,
      child: Container(
        width: MediaQuery.of(context).size.width * 0.8,
        padding: EdgeInsets.symmetric(vertical: 5, horizontal: 3),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.all(
            Radius.circular(
              30,
            ),
          ),
          border: Border.all(width: 3, color: Colors.white),
        ),
        child: Center(
          child: Text(
            label,
            style: kButtonText,
          ),
        ),
      ),
    );
  }
}

class EntryTile extends StatelessWidget {
  final String title;
  final String entry;
  final String dateTime;
  const EntryTile({
    Key? key,
    required this.title,
    required this.entry,
    required this.dateTime,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(
        10,
      ),
      margin: EdgeInsets.symmetric(
        horizontal: 10,
      ),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.all(
            Radius.circular(15),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.25),
              blurRadius: 3,
              offset: Offset(0, 7),
            )
          ]),
      child: ListTile(
        onTap: () {
          Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => ReadSingleEntry(
                  title: title,
                  entry: entry,
                  date: dateTime,
                ),
              ));
        },
        contentPadding: EdgeInsets.all(3),
        title: Text(
          title,
          style: TextStyle(
            color: Color(0xff00114f),
            fontWeight: FontWeight.w600,
            fontSize: 28,
          ),
        ),
        subtitle: Text(
          entry,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            color: Color(0xff00114f),
            fontSize: 24,
          ),
        ),
        tileColor: Colors.white,
        trailing: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${dateTime.substring(5, 11)}, ${dateTime.substring(0, 3)}',
              style: TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.w600,
                color: Color(0xff00114f),
              ),
            ),
            SizedBox(
              height: 3,
            ),
            Text(
              dateTime.substring(17).trim(),
              style: TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.w600,
                color: Color(0xff00114f),
              ),
            ),
          ],
        ),
      ),
    );
  }
}