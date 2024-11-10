const express = require('express');
const mysql = require('mysql');
const myapp = express();
const port = 3306;

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'root',
});
    
db.connect((err) => {
if (err) throw err;
    console.log('Connected to MySQL database');
});
    
app.use(express.json());

app.post('/api/students', (req, res) => {
    const { name, email, dob, gender } = req.body;
    const sql = 'INSERT INTO students (name, email, dob, gender) VALUES (?, ?, ?, ?)';
    db.query(sql, [name, email, dob, gender], (err, result) => {
    if (err) {
    console.error(err);
    res.status(500).send('Error saving data');
    } else {
    res.status(201).send('Data saved successfully');
    }
    });
    });
    
    app.listen(port, () => {
    console.log('Server is running on port ${port}');
    });
// const sqlite3 = require('sqlite3').verbose();
// const express = require('express');
// const fs = require('fs');
// const path = require('path');

// const app = express();
// const db = new sqlite3.Database('images.db');

// // Function to fetch image paths from the database
// async function getImagesForProducts(products) {
//     return new Promise((resolve, reject) => {
//       // Convert product names to a comma-separated list for the SQL query
//       const placeholders = products.map(() => '?').join(',');
//       const query = `SELECT image_name, image_path FROM images WHERE product_name IN (${placeholders}) LIMIT 5`;
  
//       db.all(query, products, (err, rows) => {
//         if (err) {
//           reject(err);
//         } else {
//           resolve(rows);
//         }
//       });
//     });
// }

// // API endpoint to get images based on model's product list
// app.get('/get-skincare-images', async (req, res) => {
//     try {
//       // Assume this list comes from your model
//       const modelProductList = ['moisturizer', 'sunscreen', 'cleanser'];
  
//       // Get image data from the database
//       const imageRecords = await getImagesForProducts(modelProductList);
  
//       // Load images from the filesystem
//       const images = imageRecords.map(record => {
//         const imagePath = path.join(__dirname, record.image_path);
//         if (fs.existsSync(imagePath)) {
//           return {
//             imageName: record.image_name,
//             imageBase64: fs.readFileSync(imagePath, { encoding: 'base64' })
//           };
//         }
//         return null;
//       }).filter(img => img !== null);
  
//       // Send the images as a JSON response
//       res.json({ images });
//     } catch (error) {
//       console.error('Error fetching images:', error);
//       res.status(500).send('Server Error');
//     }
//   });
  
//   // Start the server
//   app.listen(3000, () => console.log('Server running on port 3000'));