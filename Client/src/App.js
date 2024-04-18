//THIS IS WHERE WE PUT OUR COMPONENTS IN 
import React, { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    InstructorId: '',
    FName: '',
    LName: '',
    StartDate: '',
    Degree: '',
    Rank: '',
    Type: ''
  });

  const [studentId, setStudentId] = useState('');
  const [message1, setMessage1] = useState('');
  const [message2, setMessage2] = useState('');

  const handleInputChange = (event) => {
    setStudentId(event.target.value);
  };

  const handleDelete = () => {
    fetch(`/delete?StudentId=${studentId}`, {
      method: 'DELETE'
    })
    .then(res => res.json())
    .then(data => {
      setMessage1(data.message);
    })
    .catch(error => {
      console.error('Error deleting student:', error);
      setMessage1('Error deleting student. Please try again.');
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = () => {
    fetch('/input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      setMessage2(data)
      // Handle success response if needed
    })
    .catch(error => {
      setMessage2(error)
      console.error('Error adding instructor:', error);
      // Handle error if needed
    });
  };

  return (
    <div className="form-container">
      <div >
        <div>
          <label>
            InstructorId:
            <input
              type="text"
              name="InstructorId"
              value={formData.InstructorId}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            FName:
            <input
              type="text"
              name="FName"
              value={formData.FName}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            LName:
            <input
              type="text"
              name="LName"
              value={formData.LName}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            StartDate:
            <input
              type="text"
              name="StartDate"
              value={formData.StartDate}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            Degree:
            <input
              type="text"
              name="Degree"
              value={formData.Degree}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            Rank:
            <input
              type="text"
              name="Rank"
              value={formData.Rank}
              onChange={handleChange}
            />
          </label>
        </div>
        <div>
          <label>
            Type:
            <input
              type="text"
              name="Type"
              value={formData.Type}
              onChange={handleChange}
            />
          </label>
        </div>
        <button onClick={handleSubmit}>Add Instructor</button>
        {message2 && <div className="message">{message2.message}</div>} {/* Render message2.message */}
      </div>
  
      <div>
        <label>
          Student ID:
          <input
            type="text"
            value={studentId}
            onChange={handleInputChange}
          />
        </label>
        <button onClick={handleDelete}>Delete Student</button>
        {message1 && <div className="message">{message1}</div>}
      </div>
    </div>
  )
};

export default App