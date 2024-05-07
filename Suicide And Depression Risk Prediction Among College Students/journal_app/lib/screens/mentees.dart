import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class AnotherScreen extends StatefulWidget {
  final String selectedItem;

  const AnotherScreen({required this.selectedItem});

  @override
  _AnotherScreenState createState() => _AnotherScreenState();
}

class _AnotherScreenState extends State<AnotherScreen> {
  List<Map<String, dynamic>> documents = [];

  @override
  void initState() {
    super.initState();
    _loadDocuments();
  }

 _loadDocuments() async {
  QuerySnapshot querySnapshot = await FirebaseFirestore.instance
      .collection('/model/model/${widget.selectedItem}')
      .get();

  setState(() {
    documents = querySnapshot.docs
        .map((doc) => {'id': doc.id, 'data': doc.data()})
        .toList();
    
    // Sorting the documents list based on the 'percentage' field in descending order
    documents.sort((a, b) => (b['data']['percentage'] as int).compareTo(a['data']['percentage'] as int));
  });
}



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Mentees of ${widget.selectedItem}'),
      ),
      body: ListView.builder(
  itemCount: documents.length,
  itemBuilder: (context, index) {
    return ListTile(
      leading: Text('${index + 1}'), // Serial number
      title: Text(documents[index]['id']),
      subtitle: Text(
        'Name: ${documents[index]['data']['name']}'
      ), // Adjust the key according to your data structure
    );
  },
),

    );
  }
}
