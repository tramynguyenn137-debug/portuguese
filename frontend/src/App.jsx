import { useState, useEffect } from 'react'
import './App.css'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [page, setPage] = useState('topics') // topics | flashcard | quiz
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedTopic, setSelectedTopic] = useState(null)

  useEffect(() => {
    fetch(`${API}/topics`)
      .then(r => r.json())
      .then(data => { setTopics(data); setLoading(false) })
      .catch(() => { setError('Không thể kết nối backend. Hãy chạy backend trước!'); setLoading(false) })
  }, [])

  return (
    <div className="app">
      <header className="header">
        <span className="header-flag">🇧🇷</span>
        <h1>Tiếng Bồ Đào Nha</h1>
        <nav className="nav">
          <button className={`nav-btn ${page === 'topics' ? 'active' : ''}`} onClick={() => setPage('topics')}>
            📚 Chủ đề
          </button>
          <button className={`nav-btn ${page === 'quiz' ? 'active' : ''}`} onClick={() => { setPage('quiz'); setSelectedTopic(null) }}>
            🎯 Luyện tập
          </button>
        </nav>
      </header>

      <main className="main">
        {error && <div className="error-msg">⚠️ {error}</div>}
        {loading && <div className="loading">Đang tải...</div>}

        {!loading && !error && page === 'topics' && (
          <TopicsPage
            topics={topics}
            onSelect={t => { setSelectedTopic(t); setPage('flashcard') }}
          />
        )}

        {!loading && !error && page === 'flashcard' && selectedTopic && (
          <FlashcardPage topic={selectedTopic} onBack={() => setPage('topics')} />
        )}

        {!loading && !error && page === 'quiz' && (
          <QuizPage topics={topics} />
        )}
      </main>
    </div>
  )
}

function TopicsPage({ topics, onSelect }) {
  return (
    <>
      <h2 className="page-title">Chọn chủ đề học</h2>
      <p className="page-subtitle">Click vào chủ đề để bắt đầu học flashcard</p>
      <div className="topics-grid">
        {topics.map(t => (
          <div className="topic-card" key={t.id} onClick={() => onSelect(t)}>
            <div className="topic-icon">{t.icon}</div>
            <div className="topic-name">{t.name}</div>
            <div className="topic-desc">{t.description}</div>
            <span className="topic-count">{t.word_count} từ</span>
          </div>
        ))}
      </div>
    </>
  )
}

function FlashcardPage({ topic, onBack }) {
  const [words, setWords] = useState([])
  const [index, setIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${API}/topics/${topic.id}/words`)
      .then(r => r.json())
      .then(data => { setWords(data); setLoading(false) })
  }, [topic.id])

  if (loading) return <div className="loading">Đang tải từ vựng...</div>

  const word = words[index]
  const progress = words.length ? ((index + 1) / words.length) * 100 : 0

  return (
    <>
      <div className="flashcard-header">
        <button className="back-btn" onClick={onBack}>← Quay lại</button>
        <span className="flashcard-title">{topic.icon} {topic.name}</span>
      </div>

      <p className="progress-text">{index + 1} / {words.length}</p>
      <div className="progress-bar-wrap">
        <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
      </div>

      <div className="card-scene" onClick={() => setFlipped(f => !f)}>
        <div className={`card-inner ${flipped ? 'flipped' : ''}`}>
          <div className="card-face card-front">
            <div className="card-label">🇧🇷 Tiếng Bồ Đào Nha</div>
            <div className="card-word">{word.portuguese}</div>
            {word.example_pt && <div className="card-example">"{word.example_pt}"</div>}
            <div className="card-hint">Nhấn để xem nghĩa</div>
          </div>
          <div className="card-face card-back">
            <div className="card-label">🇻🇳 Tiếng Việt</div>
            <div className="card-word">{word.vietnamese}</div>
            {word.example_vi && <div className="card-example">"{word.example_vi}"</div>}
          </div>
        </div>
      </div>

      <div className="card-controls">
        <button
          className="ctrl-btn prev"
          disabled={index === 0}
          onClick={() => { setIndex(i => i - 1); setFlipped(false) }}
        >
          ← Trước
        </button>
        <button
          className="ctrl-btn next"
          disabled={index === words.length - 1}
          onClick={() => { setIndex(i => i + 1); setFlipped(false) }}
        >
          Tiếp →
        </button>
      </div>
    </>
  )
}

function QuizPage({ topics }) {
  const [quizTopicId, setQuizTopicId] = useState('')
  const [questions, setQuestions] = useState(null)
  const [qIndex, setQIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [chosen, setChosen] = useState(null)
  const [done, setDone] = useState(false)
  const [loading, setLoading] = useState(false)

  function startQuiz() {
    setLoading(true)
    const url = quizTopicId
      ? `${API}/words/quiz?topic_id=${quizTopicId}&count=10`
      : `${API}/words/quiz?count=10`
    fetch(url)
      .then(r => r.json())
      .then(data => { setQuestions(data); setQIndex(0); setScore(0); setChosen(null); setDone(false); setLoading(false) })
  }

  function pick(option, correct) {
    if (chosen) return
    setChosen(option)
    if (option === correct) setScore(s => s + 1)
  }

  function next() {
    if (qIndex + 1 >= questions.length) {
      setDone(true)
    } else {
      setQIndex(i => i + 1)
      setChosen(null)
    }
  }

  if (loading) return <div className="loading">Đang tải câu hỏi...</div>

  if (!questions) {
    return (
      <div className="quiz-setup">
        <h2>🎯 Luyện tập Quiz</h2>
        <p>Chọn chủ đề hoặc luyện tập tất cả từ vựng</p>
        <select className="topic-select" value={quizTopicId} onChange={e => setQuizTopicId(e.target.value)}>
          <option value="">Tất cả chủ đề</option>
          {topics.map(t => (
            <option key={t.id} value={t.id}>{t.icon} {t.name}</option>
          ))}
        </select>
        <button className="start-quiz-btn" onClick={startQuiz}>Bắt đầu!</button>
      </div>
    )
  }

  if (done) {
    const pct = Math.round((score / questions.length) * 100)
    const emoji = pct >= 80 ? '🎉' : pct >= 60 ? '😊' : '💪'
    return (
      <div className="score-screen">
        <div className="score-emoji">{emoji}</div>
        <div className="score-title">Kết quả</div>
        <div className="score-number">{score}/{questions.length}</div>
        <div className="score-sub">{pct}% chính xác</div>
        <div className="score-actions">
          <button className="score-btn primary" onClick={startQuiz}>Làm lại</button>
          <button className="score-btn secondary" onClick={() => setQuestions(null)}>Đổi chủ đề</button>
        </div>
      </div>
    )
  }

  const q = questions[qIndex]
  return (
    <>
      <p className="progress-text" style={{ color: 'rgba(255,255,255,0.8)', marginBottom: 8 }}>
        Câu {qIndex + 1} / {questions.length} &nbsp;•&nbsp; Điểm: {score}
      </p>
      <div className="progress-bar-wrap">
        <div className="progress-bar-fill" style={{ width: `${((qIndex + 1) / questions.length) * 100}%` }} />
      </div>
      <div className="quiz-card">
        <div className="quiz-question">{q.portuguese}</div>
        {q.example_pt && <div className="quiz-example">"{q.example_pt}"</div>}
        <div className="quiz-options">
          {q.options.map(opt => {
            let cls = 'quiz-option'
            if (chosen) {
              if (opt === q.correct_answer) cls += ' correct'
              else if (opt === chosen) cls += ' wrong'
              else cls += ' disabled'
            }
            return (
              <button key={opt} className={cls} onClick={() => pick(opt, q.correct_answer)}>
                {opt}
              </button>
            )
          })}
        </div>
        <div className={`quiz-feedback ${chosen ? (chosen === q.correct_answer ? 'correct' : 'wrong') : ''}`}>
          {chosen && (chosen === q.correct_answer ? '✓ Chính xác!' : `✗ Đáp án: ${q.correct_answer}`)}
        </div>
        {chosen && (
          <button className="quiz-next-btn" onClick={next}>
            {qIndex + 1 >= questions.length ? 'Xem kết quả' : 'Câu tiếp →'}
          </button>
        )}
      </div>
    </>
  )
}

export default App
