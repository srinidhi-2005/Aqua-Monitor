const User = require('../models/User');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const jwt_token = process.env.JWT_TOKEN;

const registerUser = async (req, res) => {
    try {
        const { name, email, password } = req.body;
        let user = await User.findOne({ email });
        if (user) {
          return res.status(400).json({ error: 'User already exists' });
        }
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);
        user = new User({ name, email, password: hashedPassword });
        await user.save();
        const token = jwt.sign(
          { 
            id: user._id,
            name: user.name,
            email: user.email,
          }, 
          jwt_token, 
          { expiresIn: '10h' }
        );
        res.json({ token, email: user.email, message: "Registration successful" });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
}

const loginUser = async (req, res) => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
          return res.status(400).json({ error: 'Invalid credentials' });
        }
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
          return res.status(400).json({ error: 'Invalid credentials' });
        }
        const token = jwt.sign(
          { 
            id: user._id,
            name: user.name,
            email: user.email,
          }, 
          jwt_token, 
          { expiresIn: '10h' }
        );
        res.json({ token, email: user.email, message: "Login successful" });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
}

const updatePassword = async (req, res) => {
    try {
        const { email, oldPassword, newPassword } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(400).json({ error: 'User not found' });
        }
        const isMatch = await bcrypt.compare(oldPassword, user.password);
        if (!isMatch) {
            return res.status(400).json({ error: 'Old password is incorrect' });
        }
        const salt = await bcrypt.genSalt(10);
        const hashedNewPassword = await bcrypt.hash(newPassword, salt);
        user.password = hashedNewPassword;
        await user.save();
        res.json({ message: "Password updated successfully" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
}

module.exports = { registerUser, loginUser, updatePassword };