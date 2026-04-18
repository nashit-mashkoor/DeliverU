import { Link } from 'react-router-dom'
import './Landing.css'

const telemetryStats = [
  { value: '31%', label: 'Less spent on delivery' },
  { value: '92%', label: 'Orders arriving on time' },
  { value: '1-tap', label: 'Repeats for weekly essentials' },
]

const controlMetrics = [
  { title: 'Save More', value: '-31%', detail: 'with smarter shared delivery rounds' },
  { title: 'Stress Less', value: '92%', detail: 'arrive in the promised window' },
  { title: 'Repeat Easy', value: 'Auto', detail: 'set recurring items once' },
  { title: 'Shop Better', value: '+41%', detail: 'stronger local store availability' },
]

const timeline = [
  {
    step: '01',
    title: 'Choose a time that fits your week',
    text: 'Pick a delivery slot once and plan your week around it.',
  },
  {
    step: '02',
    title: 'Add what you need and set repeats',
    text: 'Keep daily essentials on repeat so you do not reorder everything again.',
  },
  {
    step: '03',
    title: 'Track your order until it arrives',
    text: 'Follow clear status updates from scheduled to delivered.',
  },
]

const reliabilitySignals = [
  {
    signal: 'Lower cost for everyday orders',
    copy: 'Shared rounds keep delivery affordable even when your order is small.',
  },
  {
    signal: 'A delivery rhythm you can trust',
    copy: 'Scheduled windows make your routine easier to manage every week.',
  },
  {
    signal: 'Clear updates and better peace of mind',
    copy: 'Track each order and get straightforward support when something goes wrong.',
  },
]

function Landing() {
  return (
    <div className="landing-v2">
      <div className="landing-v2__wash" aria-hidden="true" />
      <div className="landing-v2__mesh" aria-hidden="true" />
      <div className="landing-v2__scanline" aria-hidden="true" />

      <header className="landing-v2__hero">
        <nav className="landing-v2__nav">
          <div className="landing-v2__brand">
            <span className="brand-mark" aria-hidden="true" />
            <span>DeliverU</span>
          </div>
          <div className="landing-v2__nav-links">
            <a href="#orchestration">Orchestration</a>
            <a href="#timeline">Workflow</a>
            <a href="#reliability">Reliability</a>
          </div>
          <Link className="landing-v2__button ghost" to="/login">
            Sign in
          </Link>
        </nav>

        <div className="landing-v2__hero-grid">
          <div className="landing-v2__copy">
            <p className="landing-v2__kicker">EVERYDAY DELIVERY, SIMPLIFIED</p>
            <h1>
              Save More.
              <span> Never Run Out.</span>
            </h1>
            <p className="landing-v2__lede">
              DeliverU helps you save on everyday delivery and keeps weekly essentials arriving on
              time, without the daily hassle.
            </p>
            <div className="landing-v2__chips" aria-label="Core capabilities">
              <span>Lower delivery cost</span>
              <span>Easy repeat orders</span>
              <span>Reliable weekly delivery</span>
            </div>
            <div className="landing-v2__actions">
              <Link className="landing-v2__button" to="/register">
                Get started
              </Link>
              <Link className="landing-v2__button secondary" to="/login">
                Sign in
              </Link>
            </div>
            <div className="landing-v2__stats">
              {telemetryStats.map((stat) => (
                <div key={stat.label}>
                  <strong>{stat.value}</strong>
                  <span>{stat.label}</span>
                </div>
              ))}
            </div>
          </div>

          <aside className="landing-v2__ops" aria-label="Live operations board">
            <div className="ops-head">
              <span>TODAY / ACTIVE ROUND</span>
              <span>ARRIVES 14:30</span>
            </div>
            <div className="ops-graph" aria-hidden="true">
              <div className="ops-path">
                <span className="node hot" />
                <span className="node" />
                <span className="node" />
                <span className="node" />
                <span className="node" />
                <span className="node hot" />
              </div>
            </div>
            <div className="ops-cards">
              <article>
                <p>Current Round</p>
                <span>12 deliveries in progress</span>
              </article>
              <article>
                <p>Delivery Load</p>
                <span>Balanced and on schedule</span>
              </article>
              <article>
                <p>Upcoming Stops</p>
                <span>4 deliveries up next</span>
              </article>
            </div>
          </aside>
        </div>
      </header>

      <section className="landing-v2__ticker" aria-hidden="true">
        <div>
          <span>lower delivery fees</span>
          <span>predictable weekly slots</span>
          <span>repeat your essentials</span>
          <span>fewer last-minute store runs</span>
          <span>lower delivery fees</span>
          <span>predictable weekly slots</span>
          <span>repeat your essentials</span>
          <span>fewer last-minute store runs</span>
        </div>
      </section>

      <section id="orchestration" className="landing-v2__matrix reveal" style={{ '--delay': '100ms' }}>
        <div className="landing-v2__heading">
          <p className="landing-v2__kicker">WHY PEOPLE SWITCH</p>
          <h2>Better value, better routine, better delivery experience.</h2>
          <p>
            DeliverU replaces expensive one-off orders with a simple weekly model that saves money
            and removes delivery guesswork.
          </p>
        </div>
        <div className="matrix-grid" aria-label="Operational metrics">
          {controlMetrics.map((metric) => (
            <article className="metric" key={metric.title}>
              <h3>{metric.title}</h3>
              <strong>{metric.value}</strong>
              <p>{metric.detail}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="timeline" className="landing-v2__timeline reveal" style={{ '--delay': '160ms' }}>
        <div className="landing-v2__heading">
          <p className="landing-v2__kicker">HOW IT WORKS</p>
          <h2>Simple to start, easy to keep running.</h2>
        </div>
        <div className="timeline-grid">
          {timeline.map((entry) => (
            <article className="timeline-step" key={entry.step}>
              <span>{entry.step}</span>
              <h3>{entry.title}</h3>
              <p>{entry.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="reliability" className="landing-v2__reliability reveal" style={{ '--delay': '220ms' }}>
        <div className="landing-v2__heading">
          <p className="landing-v2__kicker">WHY IT FEELS RELIABLE</p>
          <h2>Made for real life, not perfect days.</h2>
        </div>
        <div className="reliability-grid">
          {reliabilitySignals.map((item) => (
            <article key={item.signal}>
              <h3>{item.signal}</h3>
              <p>{item.copy}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="landing-v2__final reveal" style={{ '--delay': '300ms' }}>
        <div>
          <p className="landing-v2__kicker">READY TO SWITCH</p>
          <h2>Stop paying extra for random one-off deliveries.</h2>
          <p>
            Start using DeliverU for lower costs, easier weekly planning, and dependable delivery
            without daily effort.
          </p>
        </div>
        <div className="landing-v2__actions">
          <Link className="landing-v2__button" to="/register">
            Get started
          </Link>
          <Link className="landing-v2__button secondary" to="/login">
            Sign in
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Landing
