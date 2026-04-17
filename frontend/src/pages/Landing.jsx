import './Landing.css'

function Landing() {
  return (
    <div className="landing">
      <header className="landing-hero">
        <div className="landing-brand">DeliverU</div>
        <h1>Delivery designed for real life.</h1>
        <p>
          DeliverU is built for busy people who need reliable, affordable grocery delivery without
          daily friction. We optimize routes by planning driver slots around peak demand so multiple
          orders move in a single round. The result is lower costs, better reliability, and recurring
          orders that arrive without you having to place them every day.
        </p>
        <div className="landing-actions">
          <a className="landing-button" href="/login">Log in</a>
          <a className="landing-button secondary" href="/register">Sign up</a>
        </div>
      </header>

      <section className="landing-card">
        <h2>1. Introduction</h2>

        <h3>1.1 Product</h3>
        <p>
          In today’s fast paced and hectic lifestyle, people find themselves overworked and
          overburdened. Time has become one of the most prized luxuries of life. In such conditions,
          daily chores are hard to complete and even a simple grocery run becomes a burden. People are
          in dire need of a service that lets them fulfill their grocery requirements from the comfort
          of their homes. Unfortunately, many delivery services are overpriced, unviable for small
          orders, and require constant input for recurring needs. DeliverU aims to solve these issues
          and provide relief to such individuals.
        </p>
        <p>
          Our product lowers delivery charges by allocating specific slots for drivers to make rounds
          in predefined regions. Time slots are planned around peak demand hours. This lets multiple
          orders be handled in a single round, reducing costs and saving time for drivers. Moreover,
          the product allows recurring orders within a time slot that are delivered daily without
          having to place them each day.
        </p>

        <h3>1.2 Scope</h3>
        <p>
          The product is designed to scale into a nation-wide, cheap, and convenient delivery service.
          At all stages it will:
        </p>
        <ul>
          <li>Allow customers to make orders in predefined slots within their region.</li>
          <li>Allow customers to create recurring orders delivered daily without continuous input.</li>
          <li>Let customers order daily grocery items and local restaurant offerings.</li>
          <li>Allow admins to manage regions, time slots, and order items.</li>
          <li>Allow admins to view system analytics for business decisions.</li>
        </ul>

        <h3>1.3 Business Goals</h3>
        <p>
          The end goal is to create a profitable, scalable business while helping busy individuals
          fulfill their daily grocery requirements. DeliverU aims to:
        </p>
        <ul>
          <li>Build a cost effective and efficient delivery network.</li>
          <li>Capture market share by offering a cheaper, easy-to-use alternative.</li>
          <li>Provide delivery access to small businesses without an existing network.</li>
          <li>Develop mutually beneficial relationships with other businesses.</li>
        </ul>
      </section>
    </div>
  )
}

export default Landing
