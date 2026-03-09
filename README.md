# eGramSabha

**eGramSabha** is a Digital Public Good (DPG) designed to facilitate Gram Panchayats in conducting transparent and efficient digital Gram Sabha meetings. This tool aims to enhance local governance by leveraging technology for inclusivity, accountability, and ease of use.

---

## Features

- **Onboarding of a Gram Panchayat**: Simplify the setup process for new Gram Panchayats.
- **Add Gram Sabha Members**: Register members with ease.
- **Assign Roles**: Allocate specific roles to Gram Sabha members for better task distribution.
- **Facial Recognition Backed Biometric Authentication**: Ensure secure and reliable member verification.
- **Scheduling Gram Sabha**: Plan and manage meeting schedules effortlessly.
- **Add Issues/Concerns/Suggestions**: Collect inputs for Gram Sabha discussions.
- **Prepare Agenda**: Organize and prioritize items for discussion in the Gram Sabha.
- **Digital Gram Sabha**: Conduct meetings with biometric verification of members to meet quorum requirements.
- **Generate MOM**: Automatically generate Minutes of Meeting (MOM) from audio recordings.

---

## How to Get Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/anshuljain90/ai4bharat-empowerpanchayat.git
   cd ai4bharat-empowerpanchayat
   ```

2. **Set up MongoDB**:
   - Ensure MongoDB is installed and running on your system
   - Start MongoDB on the default port (27017)

3. **Set up Backend**:
   ```bash
   cd backend
   npm install
   npm start
   ```
   The backend server will start running on `http://localhost:5000`

4. **Set up Frontend**:
   ```bash
   cd ../frontend
   npm install
   npm start
   ```

5. **Access the Application**:
   - Open your browser and go to `http://localhost:3000`
   - The backend API will be available at `http://localhost:5000`

---

## Live Prototype

| Portal | URL | Login Details |
|--------|-----|---------------|
| **Citizen Portal** | [https://44.194.253.143/citizen/login](https://44.194.253.143/citizen/login) | Last 4 digits of Voter ID + Face scan (no password needed) |
| **Official Portal** | [https://44.194.253.143/official/login](https://44.194.253.143/official/login) | Username: configured official username, Password: same as username |
| **Admin Portal** | [https://44.194.253.143/admin/login](https://44.194.253.143/admin/login) | Username: `admin`, Password: `AdminPassword123` |

### Portal Access Details

**Admin Portal** — Full system administration
- Login with username `admin` and password `AdminPassword123`
- Manage panchayats, officials, and citizen records
- Import members via CSV, assign roles
- Sample CSV files for bulk citizen import are available in the [`demo/`](demo/) folder (`sample-10citizens.csv`, `sample-30citizens.csv`, `sample-citizens.csv`)

**Official Portal** — Gram Sabha management
- Login with the official's configured username (password is the same as the username)
- Create/manage issues, schedule Gram Sabha meetings, take biometric attendance
- Generate AI-powered agendas and issue summaries

**Citizen Portal** — Voice-first citizen participation
- Login using last 4 digits of Voter ID + face recognition (passwordless)
- Citizens must be registered by an official first (face photo captured during registration)
- Report issues via voice or text, view meeting history

### Demo Video

[Demo Video (Google Drive)](https://drive.google.com/drive/folders/1aLeLtSPIDUaoypi3TAu2tg4I-TpxVUNH)

---

## Architecture

The application follows a client-server architecture:
- **Frontend**: React.js based user interface
- **Backend**: Node.js/Express API server
- **Database**: MongoDB for data storage
- **Authentication**: JWT-based authentication with facial recognition for biometric verification

---

## Contribution Guidelines

We welcome contributions from everyone! Here's how you can help:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Make your changes and test thoroughly.
4. Submit a pull request explaining your changes.

### Code Style
- Follow the established coding patterns in the repository
- Include comments where necessary
- Write tests for new features

---

## Licensing

eGramSabha is licensed under the **Apache License, Version 2.0**. Please review the [LICENSE](LICENSE) file for detailed terms.

---

## Acknowledgements

This initiative is part of the Empower Panchayat mission, focused on leveraging technology for effective rural governance. Special thanks to the open-source community for their support.

---

## Contact

For queries or collaboration opportunities, please reach out at:  
**Anshul Jain**  
📧 [anshul_jain2008@yahoo.co.in](mailto:anshul_jain2008@yahoo.co.in)
