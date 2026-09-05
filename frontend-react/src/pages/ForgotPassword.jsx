import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import '../styles/auth.css'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)

  useEffect(() => {
    document.body.classList.add('auth-body')
    return () => document.body.classList.remove('auth-body')
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: replace with a real API call, e.g.
    // await fetch('/api/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) })
    console.log('Sending reset link to', email)
    setSent(true)
  }

  return (
    <div className="forgot-container">
      <div className="forgot-box">
        <h2>Forgot Password?</h2>
        <p>Enter your registered email address and we'll send you a password reset link.</p>

        {sent ? (
          <p style={{ color: '#6EE7FF', marginBottom: '20px' }}>
            If an account exists for {email}, a reset link is on its way.
          </p>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="input-box">
              <input
                type="email"
                placeholder="Enter your Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <button type="submit">Send Reset Link</button>
          </form>
        )}

        <div className="back-login">
          <Link to="/login">← Back to Login</Link>
        </div>
      </div>
    </div>
  )
}
