# Course Reviewer Web UI

A modern, responsive web interface for the Course Reviewer Workflow system. This UI allows users to upload course content files and receive comprehensive AI-powered evaluations using ABYA University's standardized rubric.

## Features

- **Drag & Drop File Upload**: Easy file upload with drag-and-drop support
- **File Type Validation**: Supports .txt, .md, .doc, and .docx files
- **Real-time Progress**: Visual progress indicators during analysis
- **Comprehensive Results**: Detailed evaluation results with scores and feedback
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations

## Screenshots

### Upload Interface
The clean, intuitive upload interface allows users to easily submit course content for evaluation.

### Analysis Progress
Real-time progress tracking shows the three-stage AI evaluation process:
1. Course Categorization
2. Rubric Grading
3. Score Calculation

### Results Display
Comprehensive results include:
- Final weighted score
- Pass/fail status
- Individual rubric element scores
- Category-specific feedback
- Improvement recommendations

## Quick Start

### Option 1: Simple Demo (Client-side only)
1. Open `index.html` directly in your web browser
2. Upload a course content file
3. Click "Analyze Course Content"
4. View the demo results

### Option 2: Full Server Integration
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask server:
   ```bash
   python server.py
   ```

3. Open your browser to `http://localhost:5000`

4. Upload and analyze course content with backend integration

## File Structure

```
web-ui/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and animations
├── script.js           # JavaScript functionality
├── server.py           # Flask backend server
├── requirements.txt    # Python dependencies
├── sample-course.txt   # Sample course content for testing
└── README.md          # This file
```

## Supported File Types

- **Text files** (.txt)
- **Markdown files** (.md)
- **Microsoft Word** (.doc, .docx)

Maximum file size: 10MB

## API Integration

The web UI can integrate with the Course Reviewer Workflow in two ways:

### Demo Mode (Default)
Uses sample evaluation results for demonstration purposes. Perfect for showcasing the UI and evaluation format.

### Production Mode
Integrates with the actual deployed Course Reviewer Workflow on Google Cloud Vertex AI. To enable:

1. Set the `COURSE_REVIEWER_RESOURCE_ID` environment variable
2. Ensure the Poetry environment and dependencies are available
3. Uncomment the production code in `server.py`

## Customization

### Styling
Modify `styles.css` to customize:
- Color scheme and gradients
- Typography and spacing
- Animation effects
- Responsive breakpoints

### Functionality
Modify `script.js` to customize:
- File validation rules
- Progress animations
- Results display format
- API integration

### Backend
Modify `server.py` to customize:
- API endpoints
- Integration with Course Reviewer Workflow
- Session management
- Error handling

## Sample Course Content

Use the included `sample-course.txt` file to test the evaluation system. This file contains a comprehensive blockchain course description that will be categorized as "Blockchain Technology and Development" and receive detailed rubric-based evaluation.

## Browser Compatibility

- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

## Responsive Design

The interface adapts to different screen sizes:
- **Desktop** (1200px+): Full layout with side-by-side elements
- **Tablet** (768px-1199px): Stacked layout with adjusted spacing
- **Mobile** (320px-767px): Single-column layout optimized for touch

## Technology Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox/grid
- **JavaScript**: ES6+ with async/await
- **Font Awesome**: Icon library
- **Google Fonts**: Inter font family

### Backend (Optional)
- **Flask**: Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management

## Development

To extend or modify the web UI:

1. **Adding new file types**: Update the validation in `handleFile()` function
2. **Modifying the results display**: Update `displayResults()` and related functions
3. **Changing the UI theme**: Modify CSS custom properties and gradient definitions
4. **Adding new API endpoints**: Extend the Flask server in `server.py`

## Security Considerations

- File upload validation and size limits
- CORS configuration for cross-origin requests
- Input sanitization for uploaded content
- Rate limiting for API endpoints (in production)

## Security Requirements

⚠️ **IMPORTANT**: Before running the web UI, ensure you have properly configured your environment variables in the parent directory's `.env` file. Never commit API keys or sensitive credentials to version control.

The web UI requires access to the Google Cloud deployment, which needs proper authentication through environment variables.

## Performance

- Lazy loading of large result sets
- Efficient DOM manipulation
- CSS animations with GPU acceleration
- Minimal JavaScript bundle size

## Accessibility

- Semantic HTML structure
- Keyboard navigation support
- Screen reader compatible
- High contrast color ratios
- Focus indicators for interactive elements

## Future Enhancements

- **Batch Processing**: Upload multiple files at once
- **History**: View previous evaluation results
- **Export**: Download results as PDF or JSON
- **Comparison**: Compare multiple course evaluations
- **Analytics**: Dashboard with evaluation statistics
- **User Accounts**: Personal evaluation history

## Support

For issues or questions about the web UI:
1. Check the browser console for error messages
2. Verify file types and sizes are within limits
3. Ensure network connectivity for API calls
4. Review the Flask server logs for backend issues
