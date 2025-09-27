# AI-Powered Student Dashboard

A modern, full-stack web application that leverages Oracle Cloud Infrastructure (OCI) Generative AI to help students process and understand their study materials through intelligent summarization, quiz generation, and Q&A creation.

## 🚀 Features

- **Secure Authentication**: JWT-based user authentication with role-based access control
- **Document Upload**: Support for PDF, images, and text files with OCI Object Storage
- **AI-Powered Processing**: 
  - Document summarization
  - Quiz generation with multiple-choice questions
  - Simple explanations for complex concepts
  - Q&A pair generation
- **Modern UI**: Built with React and Material-UI for a responsive, intuitive experience
- **Admin Panel**: Complete user management and system monitoring
- **Cloud-Native**: Designed for Oracle Cloud Infrastructure deployment

## 🏗️ Architecture

### Backend (Node.js + Express)
- RESTful API with JWT authentication
- MySQL database with comprehensive schema
- OCI Object Storage integration for file management
- OCI Generative AI service integration
- Role-based access control (Student/Admin)

### Frontend (React + TypeScript)
- Modern React with TypeScript
- Material-UI components for consistent design
- Context-based state management
- Responsive design for all devices

### Database Schema
- Users and profiles management
- File upload tracking
- AI job processing queue
- Admin activity logging
- Role-based permissions

## 🛠️ Tech Stack

### Backend
- Node.js
- Express.js
- MySQL
- JWT Authentication
- OCI SDK
- Multer (file uploads)
- Bcrypt (password hashing)

### Frontend
- React 18
- TypeScript
- Material-UI
- React Router
- Axios
- React Dropzone

### Infrastructure
- Oracle Cloud Infrastructure
- OCI Object Storage
- OCI Generative AI
- MySQL Database

## 📦 Installation

### Prerequisites
- Node.js (v16 or higher)
- MySQL (v8.0 or higher)
- Oracle Cloud Infrastructure account
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-student-dashboard.git
   cd ai-student-dashboard
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Configure environment variables**
   ```bash
   cd server
   cp env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   # Database Configuration
   DB_HOST=localhost
   DB_USER=your_mysql_user
   DB_PASSWORD=your_mysql_password
   DB_NAME=student_dashboard

   # JWT Configuration
   JWT_SECRET=your_super_secret_jwt_key_here
   JWT_EXPIRES_IN=7d

   # Server Configuration
   PORT=5000
   NODE_ENV=development

   # OCI Configuration
   OCI_REGION=us-ashburn-1
   OCI_TENANCY_OCID=ocid1.tenancy.oc1..your_tenancy_ocid
   OCI_USER_OCID=ocid1.user.oc1..your_user_ocid
   OCI_FINGERPRINT=your_api_key_fingerprint
   OCI_PRIVATE_KEY_PATH=./oci-private-key.pem
   OCI_COMPARTMENT_OCID=ocid1.compartment.oc1..your_compartment_ocid
   OCI_NAMESPACE=your_namespace
   OCI_BUCKET_NAME=student-dashboard-uploads
   OCI_GENERATIVE_AI_ENDPOINT=https://generativeai.oci.oraclecloud.com
   OCI_GENERATIVE_AI_MODEL_ID=cohere.command-text-14b
   ```

4. **Set up OCI credentials**
   - Create an API key in OCI Console
   - Download the private key file
   - Place it in the `server` directory as `oci-private-key.pem`
   - Update the OCI configuration in `.env`

5. **Create MySQL database**
   ```sql
   CREATE DATABASE student_dashboard;
   ```

6. **Start the backend server**
   ```bash
   cd server
   npm run dev
   ```

### Frontend Setup

1. **Navigate to client directory**
   ```bash
   cd client
   ```

2. **Install dependencies** (if not done already)
   ```bash
   npm install
   ```

3. **Configure API endpoint**
   Create `client/.env`:
   ```env
   REACT_APP_API_URL=http://localhost:5000/api
   ```

4. **Start the development server**
   ```bash
   npm start
   ```

## 🚀 Deployment

### OCI Deployment

1. **Set up OCI resources**:
   - Create a VCN and subnet
   - Set up a MySQL instance (or use OCI MySQL)
   - Create Object Storage buckets
   - Configure IAM policies

2. **Deploy backend**:
   - Use OCI Container Instances or Compute instances
   - Configure environment variables
   - Set up load balancer if needed

3. **Deploy frontend**:
   - Build the React app: `npm run build`
   - Deploy to OCI Web Apps or static hosting
   - Configure CDN for better performance

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY server/package*.json ./
RUN npm install
COPY server/ .
EXPOSE 5000
CMD ["npm", "start"]
```

## 📱 Usage

1. **Register/Login**: Create an account or sign in
2. **Upload Documents**: Upload PDF, images, or text files
3. **AI Processing**: Choose from summarization, quiz generation, or Q&A creation
4. **View Results**: Access processed content in your dashboard
5. **Admin Features**: Manage users and monitor system activity (admin only)

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### File Management
- `POST /api/upload` - Upload file
- `GET /api/upload` - Get user uploads
- `DELETE /api/upload/:id` - Delete upload

### AI Processing
- `POST /api/ai/generate` - Generate AI content
- `GET /api/ai/jobs` - Get AI jobs
- `GET /api/ai/jobs/:id` - Get specific AI job results

### Admin
- `GET /api/admin/users` - Get all users
- `GET /api/admin/stats` - Get system statistics
- `PUT /api/admin/users/:id/toggle-status` - Toggle user status
- `DELETE /api/admin/users/:id` - Delete user

## 🛡️ Security Features

- JWT token authentication
- Password hashing with bcrypt
- Role-based access control
- File type validation
- Rate limiting
- CORS protection
- Input validation and sanitization

## 📊 Database Schema

The application uses a comprehensive MySQL schema with the following main tables:
- `users` - User accounts
- `profiles` - User profile information
- `uploads` - File upload metadata
- `ai_jobs` - AI processing jobs
- `ai_results` - AI processing results
- `admin_logs` - Administrative actions
- `roles` - User roles and permissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Portfolio Showcase

This project demonstrates:
- **Full-Stack Development**: Complete React + Node.js application
- **Cloud Integration**: Oracle Cloud Infrastructure services
- **AI/ML Integration**: Generative AI for educational content
- **Modern UI/UX**: Material-UI design system
- **Database Design**: Comprehensive relational schema
- **Security**: JWT authentication and role-based access
- **Scalability**: Cloud-native architecture
- **TypeScript**: Type-safe development

## 📞 Contact

Your Name - [@yourusername](https://github.com/yourusername) - your.email@example.com

Project Link: [https://github.com/yourusername/ai-student-dashboard](https://github.com/yourusername/ai-student-dashboard)

## 🙏 Acknowledgments

- Oracle Cloud Infrastructure for cloud services
- Material-UI for the component library
- React team for the amazing framework
- The open-source community for various packages used
