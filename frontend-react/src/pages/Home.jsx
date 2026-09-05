import { useState } from 'react'
import { Link } from 'react-router-dom'
import '../styles/main.css'

const SAMPLE_SONGS = [
  { id: 1, title: 'Main agar kahun', desc: 'desc', img: '/images/1.png' },
  { id: 2, title: 'Main agar kahun', desc: 'desc', img: '/images/2.png' },
  { id: 3, title: 'Main agar kahun', desc: 'desc', img: '/images/3.png' },
  { id: 4, title: 'Main agar kahun', desc: 'desc', img: '/images/4.png' },
  { id: 5, title: 'Main agar kahun', desc: 'desc', img: '/images/5.png' },
  { id: 6, title: 'Main agar kahun', desc: 'desc', img: '/images/6.png' },
  { id: 7, title: 'Main agar kahun', desc: 'desc', img: '/images/1.png' },
]

const SECTIONS = ['Popular songs', 'Popular songs', 'Popular songs', 'Popular songs', 'Popular songs', 'Popular songs']

const MOODS = ['😊', '😍', '😎', '😢', '😴', '😡']

export default function Home() {
  const [searchTerm, setSearchTerm] = useState('')
  const [currentSong, setCurrentSong] = useState({ title: 'Believer', artist: 'Imagine Dragons', img: '/images/default-song.jpg' })
  const [isPlaying, setIsPlaying] = useState(false)
  const [isShuffle, setIsShuffle] = useState(false)
  const [isRepeat, setIsRepeat] = useState(false)
  const [isFavorite, setIsFavorite] = useState(false)
  const [activeMood, setActiveMood] = useState(null)
  const [volume, setVolume] = useState(70)
  const [progress, setProgress] = useState(30)

  const playSong = (song) => {
    setCurrentSong({ title: song.title, artist: 'Unknown Artist', img: song.img })
    setIsPlaying(true)
  }

  const togglePlay = () => setIsPlaying((prev) => !prev)

  return (
    <>
      <nav>
        <div className="left-half">
          <div className="logo">
            <i className="fa-brands fa-itunes-note"></i>
          </div>

          <div className="home">
            <i className="fa-solid fa-house"></i>
          </div>

          <div className="search">
            <div className="search-icon">
              <i className="fa-solid fa-magnifying-glass"></i>
            </div>
            <input
              type="text"
              className="input-box"
              placeholder="Search to listen"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="right-half">
          <div className="right-half_pt-1">
            <div className="voice-assis">
              <i className="fa-solid fa-microphone"></i>
            </div>
            <div className="download">
              <i className="fa-solid fa-circle-arrow-down"></i>
              <span>Download</span>
            </div>
          </div>
          <div className="right-half_pt-2">
            <button className="settings-button">
              <Link to="/settings">
                <i className="fa-solid fa-gear"></i>
              </Link>
            </button>
            <button className="login-button">
              <Link to="/login">Login</Link>
            </button>
          </div>
        </div>
      </nav>

      <div className="main">
        <div className="main-left-part">
          <div className="library">
            <p>Your Library</p>
          </div>

          <div className="box-container">
            <div className="box">
              <h4>Create Your Playlist</h4>
              <button>Create Playlist</button>
            </div>

            <div className="box">
              <h4>Favorite Songs</h4>
              <i
                className={`fa-solid fa-heart ${isFavorite ? 'active' : ''}`}
                onClick={() => setIsFavorite((prev) => !prev)}
              ></i>
            </div>
          </div>
        </div>

        <div className="main-right-part">
          {SECTIONS.map((sectionTitle, sIndex) => (
            <div className="music-section" key={sIndex}>
              <h2>{sectionTitle}</h2>
              <div className="songs">
                {SAMPLE_SONGS.map((song) => (
                  <div className="music-card" key={`${sIndex}-${song.id}`}>
                    <img src={song.img} alt={song.title} />
                    <button className="music-play-btn" onClick={() => playSong(song)}>
                      <i className="fa-solid fa-circle-play"></i>
                    </button>
                    <div className="img-title">{song.title}</div>
                    <div className="img-description">{song.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          <div className="corner">
            <div className="ai_mood_detector">
              <h2>AI Mood</h2>
              <div className="moods">
                {MOODS.map((mood, i) => (
                  <button
                    key={i}
                    className={`mood ${activeMood === i ? 'active' : ''}`}
                    onClick={() => setActiveMood(i)}
                  >
                    {mood}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="music-control">
        <div className="song-info">
          <img src={currentSong.img} alt="Album Cover" />
          <div className="song-text">
            <h4>{currentSong.title}</h4>
            <p>{currentSong.artist}</p>
          </div>
          <button className="icon-btn" onClick={() => setIsFavorite((prev) => !prev)}>
            <i className={isFavorite ? 'fa-solid fa-heart' : 'fa-regular fa-heart'}></i>
          </button>
        </div>

        <div className="player">
          <div className="player-buttons">
            <button className={`icon-btn ${isShuffle ? 'active' : ''}`} onClick={() => setIsShuffle((p) => !p)}>
              <i className="fa-solid fa-shuffle"></i>
            </button>
            <button className="icon-btn">
              <i className="fa-solid fa-backward-step"></i>
            </button>
            <button className="play-btn" onClick={togglePlay}>
              <i className={isPlaying ? 'fa-solid fa-pause' : 'fa-solid fa-play'}></i>
            </button>
            <button className="icon-btn">
              <i className="fa-solid fa-forward-step"></i>
            </button>
            <button className={`icon-btn ${isRepeat ? 'active' : ''}`} onClick={() => setIsRepeat((p) => !p)}>
              <i className="fa-solid fa-repeat"></i>
            </button>
          </div>

          <div className="progress-bar">
            <span>0:00</span>
            <input
              type="range"
              value={progress}
              onChange={(e) => setProgress(Number(e.target.value))}
            />
            <span>3:48</span>
          </div>
        </div>

        <div className="right-controls">
          <button className="icon-btn">
            <i className="fa-solid fa-microphone"></i>
          </button>
          <button className="icon-btn">
            <i className="fa-solid fa-list"></i>
          </button>
          <button className="icon-btn">
            <i className="fa-solid fa-volume-high"></i>
          </button>
          <input
            type="range"
            value={volume}
            onChange={(e) => setVolume(Number(e.target.value))}
          />
        </div>
      </div>
    </>
  )
}
