const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

app.post('/login', (req, res) => {
    const { email, password } = req.body;
    //这里应该改为某种判断……
    if (email === 'user@example.com' && password === 'password123') {
        res.json({ success: true, token: 'someRandomToken123' });
    } else {
        res.json({ success: false, message: 'Invalid credentials' });
    }
});

app.listen(3000, () => console.log('Server running on port 3000'));