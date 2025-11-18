# Lost & Found Portal - Setup Guide

This guide will help you set up and run the Lost & Found Portal in NetBeans 16.

## Prerequisites

### Required Software
- **Java 17 or higher** - Download from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [OpenJDK](https://openjdk.org/)
- **NetBeans 16** - Download from [Apache NetBeans](https://netbeans.apache.org/download/)
- **Maven 3.6+** - Usually included with NetBeans
- **Git** - For cloning the repository

### Optional Software
- **ActiveMQ** - For JMS email notifications
- **MySQL/PostgreSQL** - For production database

## Step-by-Step Setup

### 1. Download and Install NetBeans 16

1. Go to [Apache NetBeans Downloads](https://netbeans.apache.org/download/)
2. Download NetBeans 16 with Java EE support
3. Install following the installation wizard
4. Ensure Java 17 is selected during installation

### 2. Clone the Project

```bash
# Using Git command line
git clone <repository-url>
cd lost-found-portal

# Or download as ZIP and extract
```

### 3. Open Project in NetBeans

1. Launch NetBeans 16
2. Go to **File** → **Open Project**
3. Navigate to the project directory
4. Select the project folder
5. Click **Open Project**

### 4. Configure Project Settings

#### Maven Configuration
1. Right-click on the project
2. Select **Properties**
3. Go to **Sources** → **Source/Binary Format**
4. Ensure **Source/Binary Format** is set to **17**
5. Click **OK**

#### Server Configuration
1. Go to **Tools** → **Servers**
2. Add a new server (Tomcat 10+ recommended)
3. Configure server settings
4. Assign the server to the project

### 5. Resolve Dependencies

1. Right-click on the project
2. Select **Clean and Build**
3. Wait for Maven to download all dependencies
4. Check the **Output** window for any errors

### 6. Database Setup

The application uses H2 in-memory database by default. No additional setup required.

#### Optional: External Database
To use MySQL or PostgreSQL:

1. Add database driver to `pom.xml`:
```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

2. Update `persistence.xml`:
```xml
<property name="jakarta.persistence.jdbc.driver" value="com.mysql.cj.jdbc.Driver"/>
<property name="jakarta.persistence.jdbc.url" value="jdbc:mysql://localhost:3306/lostfound"/>
<property name="jakarta.persistence.jdbc.user" value="your_username"/>
<property name="jakarta.persistence.jdbc.password" value="your_password"/>
```

### 7. Email Configuration (Optional)

#### Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Set system properties in NetBeans:
   - Right-click project → **Properties**
   - Go to **Run** → **VM Options**
   - Add: `-Demail.username=your-email@gmail.com -Demail.password=your-app-password`

#### Other SMTP Providers
Update `EmailService.java` with your SMTP settings:
```java
private static final String SMTP_HOST = "your-smtp-host";
private static final String SMTP_PORT = "587";
private static final String SMTP_USERNAME = "your-username";
private static final String SMTP_PASSWORD = "your-password";
```

### 8. JMS Setup (Optional)

#### Install ActiveMQ
1. Download ActiveMQ from [Apache ActiveMQ](https://activemq.apache.org/)
2. Extract to a directory
3. Start ActiveMQ:
```bash
# Windows
bin\activemq.bat start

# Linux/Mac
bin/activemq start
```

4. Access the admin console at `http://localhost:8161/admin`
5. Default credentials: admin/admin

### 9. Run the Application

#### Method 1: NetBeans Run
1. Right-click on the project
2. Select **Run**
3. Wait for the application to start
4. Open browser to `http://localhost:8080/lost-found-portal`

#### Method 2: Debug Mode
1. Right-click on the project
2. Select **Debug**
3. Set breakpoints as needed
4. Use the debugger to step through code

### 10. Verify Installation

1. **Home Page**: Should display the landing page with statistics
2. **Items Page**: Should show found items (initially empty)
3. **Claims Page**: Should show claims (initially empty)
4. **Admin Page**: Should show admin panel
5. **API**: Test at `http://localhost:8080/lost-found-portal/api/items`

## Troubleshooting

### Common Issues

#### 1. Java Version Mismatch
**Error**: "Unsupported major.minor version"
**Solution**: Ensure Java 17 is installed and selected in NetBeans

#### 2. Maven Dependencies Not Downloading
**Error**: "Could not resolve dependencies"
**Solution**: 
- Check internet connection
- Clear Maven cache: `mvn clean`
- Update Maven settings

#### 3. Server Won't Start
**Error**: "Port already in use"
**Solution**: 
- Change server port in server configuration
- Kill existing Java processes
- Use different port in `web.xml`

#### 4. Database Connection Issues
**Error**: "Unable to connect to database"
**Solution**:
- Check H2 database configuration
- Verify database file permissions
- Check `persistence.xml` settings

#### 5. Email Not Sending
**Error**: "Authentication failed"
**Solution**:
- Verify email credentials
- Check SMTP settings
- Enable "Less secure app access" or use App Password

#### 6. JMS Connection Failed
**Error**: "Could not connect to broker"
**Solution**:
- Ensure ActiveMQ is running
- Check broker URL in `JMSEmailService.java`
- Verify firewall settings

### Debug Steps

1. **Check NetBeans Output Window**:
   - Look for error messages
   - Check server logs
   - Verify Maven build output

2. **Verify Configuration**:
   - Check `web.xml` settings
   - Verify `persistence.xml` configuration
   - Confirm server settings

3. **Test Components Individually**:
   - Test database connection
   - Test email service
   - Test JMS connection

4. **Check Logs**:
   - Application server logs
   - Database logs
   - Email service logs

## Development Tips

### 1. Hot Reload
- Enable hot reload in NetBeans
- Changes to JSP files will be reflected immediately
- Java class changes require restart

### 2. Database Management
- Use H2 console: `http://localhost:8080/lost-found-portal/h2-console`
- JDBC URL: `jdbc:h2:mem:lostfound`
- Username: `sa`, Password: (empty)

### 3. API Testing
- Use Postman or curl to test API endpoints
- Check API documentation at `/api/items`
- Test with different HTTP methods

### 4. Image Upload
- Images are stored in `webapp/uploads/` directory
- Supported formats: JPG, PNG, GIF, BMP, WEBP
- Maximum file size: 10MB

## Production Deployment

### 1. Build WAR File
```bash
mvn clean package
```

### 2. Deploy to Application Server
- Copy WAR file to server deployment directory
- Configure production database
- Set up email and JMS services
- Configure security settings

### 3. Environment Variables
Set the following environment variables:
- `DATABASE_URL`: Production database URL
- `EMAIL_USERNAME`: SMTP username
- `EMAIL_PASSWORD`: SMTP password
- `JMS_BROKER_URL`: JMS broker URL

## Support

If you encounter issues:

1. Check this setup guide
2. Review the main README.md
3. Check NetBeans documentation
4. Search for similar issues online
5. Create an issue in the project repository

## Next Steps

After successful setup:

1. Explore the application features
2. Test the API endpoints
3. Customize the UI and functionality
4. Add your own features
5. Deploy to production

Happy coding! 🚀