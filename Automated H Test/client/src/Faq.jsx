// FAQPage.jsx
import React from 'react';
import './Faq.css';

function FAQPage() {
  return (
    <div className="faq-page">
      <h1>FAQ</h1>
      <div className="faq-list">
        <div className="faq-item">
          <h2>How do I schedule a driving test?</h2>
          <p>To schedule a driving test, you will need to contact your local RTO office or visit our website to find information on scheduling procedures and available appointment slots.</p>
        </div>
        <div className="faq-item">
          <h2>What documents do I need to bring to my driving test?</h2>
          <p>Typically, you will need to bring your learner's permit, proof of identity, proof of insurance, and any required forms or paperwork provided by your state's RTO.</p>
        </div>
        <div className="faq-item">
          <h2>How should I prepare for my driving test?</h2>
          <p>It's important to practice driving regularly and review the rules of the road. You may also consider taking driving lessons with a certified instructor to improve your skills and confidence.</p>
        </div>
        <div className="faq-item">
          <h2>What happens if I fail my driving test?</h2>
          <p>If you fail your driving test, you will usually have the opportunity to retake the test after a waiting period determined by your state's RTO. Be sure to review any feedback provided by the examiner to help you improve for your next attempt.</p>
        </div>
      </div>
    </div>
  );
}

export default FAQPage;
