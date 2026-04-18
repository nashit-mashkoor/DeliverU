import './Landing.css'

function Landing() {
  return (
    <div className="landing">
      <div className="landing-noise" aria-hidden="true" />
      <div className="landing-glow" aria-hidden="true" />
      <div className="landing-grid" aria-hidden="true" />
      <div className="landing-scanlines" aria-hidden="true" />
      <div className="landing-route-ribbon" aria-hidden="true">
        <span className="ribbon-node" />
        <span className="ribbon-node" />
        <span className="ribbon-node" />
        <span className="ribbon-node" />
      </div>

      <header className="landing-hero">
        <nav className="landing-nav">
          <div className="landing-brand">DeliverU</div>
          <div className="landing-nav-links">
            <span>Routes</span>
            <span>How it works</span>
            <span>Campus</span>
          </div>
          <button className="landing-button ghost" type="button">Log in</button>
        </nav>

        <div className="landing-hero-grid">
          <div className="landing-hero-copy">
            <div className="landing-tag">Scheduled rounds for predictable delivery.</div>
            <h1>
              Set your route.
              <span> We run the loop.</span>
            </h1>
            <p>
              DeliverU groups nearby orders into timed rounds so deliveries are faster, cheaper,
              and consistent. Choose a weekly slot once and keep it week after week.
            </p>
            <div className="landing-chips">
              <span>Shared routes</span>
              <span>Locked time slots</span>
              <span>Transparent pricing</span>
            </div>
            <div className="landing-actions">
              <button className="landing-button" type="button">Sign up</button>
              <button className="landing-button secondary" type="button">Log in</button>
            </div>
            <div className="landing-stats">
              <div>
                <span className="stat-value">4.9</span>
                <span className="stat-label">avg rider score</span>
              </div>
              <div>
                <span className="stat-value">12 min</span>
                <span className="stat-label">mean handoff</span>
              </div>
              <div>
                <span className="stat-value">72%</span>
                <span className="stat-label">recurring orders</span>
              </div>
            </div>
          </div>

          <div className="landing-hero-card" aria-hidden="true">
            <div className="route-ribbon">
              <span>Round 04 · West Loop</span>
              <span>ETA 14:30</span>
            </div>
            <div className="hero-map">
              <div className="map-node active" />
              <div className="map-node" />
              <div className="map-node" />
              <div className="map-node" />
              <div className="map-node" />
            </div>
            <div className="hero-card-stack">
              <div className="stack-card">
                <p>Groceries · 6 items</p>
                <span>Arrives in 2 rounds</span>
              </div>
              <div className="stack-card">
                <p>Pharmacy · essentials</p>
                <span>Synced to Friday</span>
              </div>
              <div className="stack-card">
                <p>Meal kit · 2 boxes</p>
                <span>Auto-locked</span>
              </div>
            </div>
            <div className="hero-pulse" aria-hidden="true" />
          </div>
        </div>
      </header>

      <section className="landing-route reveal" style={{ '--delay': '80ms' }}>
        <div className="section-label">Route 01</div>
        <div>
          <h2>One loop, fewer miles.</h2>
          <p>
            Orders on the same route move together, cutting wasted trips and stabilizing fees. The
            loop keeps ETAs accurate and handoffs smooth.
          </p>
        </div>
        <div className="route-strip" aria-hidden="true">
          <span>Round 01</span>
          <span>Round 02</span>
          <span>Round 03</span>
          <span>Round 04</span>
        </div>
      </section>

      <section className="landing-marquee" aria-hidden="true">
        <div className="marquee-track">
          <span>Shared routes · locked slots · no extra fees · live loop tracking ·</span>
          <span>Shared routes · locked slots · no extra fees · live loop tracking ·</span>
        </div>
      </section>

      <section className="landing-features reveal" style={{ '--delay': '140ms' }}>
        <div className="section-label">Core features</div>
        <article className="feature-card">
          <h3>Batch smarter.</h3>
          <p>Groceries, pharmacy, and meal kits ride the same loop.</p>
        </article>
        <article className="feature-card">
          <h3>Hold your time.</h3>
          <p>Pick a recurring slot and keep it with no rebooking.</p>
        </article>
        <article className="feature-card">
          <h3>Track the loop.</h3>
          <p>See where the round is and when your stop is next.</p>
        </article>
      </section>

      <section className="landing-steps reveal" style={{ '--delay': '220ms' }}>
        <div className="section-label">Workflow</div>
        <div className="steps-head">
          <h2>How it works</h2>
          <p>Simple for roommates, reliable enough for a routine.</p>
        </div>
        <div className="steps-grid">
          <div className="step">
            <span className="step-index">01</span>
            <h4>Choose a round</h4>
            <p>Pick a window that fits your week.</p>
          </div>
          <div className="step">
            <span className="step-index">02</span>
            <h4>Build the list</h4>
            <p>Add essentials now and set repeats for next time.</p>
          </div>
          <div className="step">
            <span className="step-index">03</span>
            <h4>Meet the drop</h4>
            <p>We combine nearby orders and deliver on the shared loop.</p>
          </div>
        </div>
      </section>

      <section className="landing-signal reveal" style={{ '--delay': '260ms' }}>
        <div className="section-label">Live rounds</div>
        <div className="signal-head">
          <h2>Signal board</h2>
          <p>Live rounds with real capacity and live routing.</p>
        </div>
        <div className="signal-grid" aria-hidden="true">
          <div className="signal-card">
            <span>Now</span>
            <h4>Campus run</h4>
            <p>Late night essentials · 9 drops</p>
          </div>
          <div className="signal-card accent">
            <span>14:30</span>
            <h4>West Loop</h4>
            <p>Groceries + pharmacy · 12 stops</p>
          </div>
          <div className="signal-card">
            <span>19:10</span>
            <h4>Studio belt</h4>
            <p>Meal kits · 6 drops</p>
          </div>
          <div className="signal-card">
            <span>Tomorrow</span>
            <h4>Morning reset</h4>
            <p>Breakfast + matcha · 15 stops</p>
          </div>
        </div>
      </section>

      <section className="landing-social reveal" style={{ '--delay': '300ms' }}>
        <div className="section-label">Social proof</div>
        <div>
          <h2>Built for shared living.</h2>
          <p>Split orders, share slots, and keep receipts in one link.</p>
        </div>
        <div className="social-cards">
          <div className="social-card">
            <span>"We save a night every week."</span>
            <p>Hana · North Dorm</p>
          </div>
          <div className="social-card">
            <span>"The loop makes it feel inevitable."</span>
            <p>Jai · Studio 504</p>
          </div>
        </div>
      </section>

      <section className="landing-final reveal" style={{ '--delay': '380ms' }}>
        <div className="section-label">Get started</div>
        <div>
          <h2>Lock your next round.</h2>
          <p>Choose a slot, build your list, and let DeliverU run the loop.</p>
        </div>
        <div className="landing-actions">
          <button className="landing-button" type="button">Sign up</button>
          <button className="landing-button secondary" type="button">Log in</button>
        </div>
      </section>
    </div>
  )
}

export default Landing
