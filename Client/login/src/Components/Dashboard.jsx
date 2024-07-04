// Dashboard.js

import React from "react";
import Topbar from "./Topbar";
import './Dashboard.css'

const Dashboard = () => {
  return (
    <div>
      <Topbar logotext="Dashboard" />

      <div className="dashboard-content">
        <h2>Welcome to your Dashboard!</h2>

        <div className="dashboard-stats">
          <div className="stat-card">
            <h3>Total Orders</h3>
            <p>120</p>
          </div>
          <div className="stat-card">
            <h3>Revenue</h3>
            <p>$12,500</p>
          </div>
          <div className="stat-card">
            <h3>Customers</h3>
            <p>500</p>
          </div>
        </div>

        <div className="recent-orders">
          <h3>Recent Orders</h3>
          <ul>
            <li>
              Order #1234 - $150 - <span>Delivered</span>
            </li>
            <li>
              Order #1235 - $200 - <span>Processing</span>
            </li>
            <li>
              Order #1236 - $100 - <span>Shipped</span>
            </li>
            <li>
              Order #1237 - $80 - <span>Delivered</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;


