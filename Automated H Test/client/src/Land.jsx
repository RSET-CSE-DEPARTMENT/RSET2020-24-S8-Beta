import React from 'react'

import './land.css'
import Navbar from './assets/components/Navbar/navbar';
const Land = () => {
 
   

  return (
    <div>
        <Navbar />
        <div className="landing-page">
            
      <header className="header">
        <h1>Driving Test </h1>
        <p>Prepare for your driving test with ease!</p>
      </header>
      <div className='fea'>
      <section className="features">
        <div className="feature">
          <h2>Practice Tests</h2>
          <p>Access a wide range of practice tests to help you prepare for your driving test.</p>
        </div>
        <div className="feature">
          <h2>Study Materials</h2>
          <p>Explore comprehensive study materials including guides, videos, and interactive quizzes.</p>
        </div>
        <div className="feature">
          <h2>Progress Tracking</h2>
          <p>Track your progress and identify areas for improvement with our progress tracking tools.</p>
        </div>
      </section>
      </div>
      
      <footer className="footer">
        <p>© 2024 Driving Test Web. All rights reserved.</p>
      </footer>
    </div>
    </div>
    
    
  )
}

export default Land
