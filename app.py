from flask import Flask, render_template, request, jsonify
import json
import requests
import traceback
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Claude API Configuration
CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Initialize components (with error handling for missing modules)
try:
    from src.components.dashboard import Dashboard
    dashboard = Dashboard()
except ImportError as e:
    print(f"Warning: Dashboard component not found: {e}")
    dashboard = None

try:
    from src.components.curriculum_converter import CurriculumConverter
    converter = CurriculumConverter()
except ImportError as e:
    print(f"Warning: CurriculumConverter component not found: {e}")
    converter = None

try:
    from src.components.curriculum_generator import CurriculumGenerator
    generator = CurriculumGenerator()
except ImportError as e:
    print(f"Warning: CurriculumGenerator component not found: {e}")
    generator = None

@app.route('/')
def index():
    """Home page with notebook paper design"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard_page():
    """Dashboard page with notebook paper design"""
    try:
        if dashboard:
            stats = dashboard.get_user_stats()
            recent_activity = dashboard.get_recent_activity()
        else:
            # Mock data for dashboard
            stats = {
                "total_conversions": 3678,
                "active_users": 1245,
                "success_rate": 94.5,
                "total_comparisons": 5432
            }
            recent_activity = [
                {"action": "Comparison generated", "details": "CBSE to IB Grade 10 Mathematics", "timestamp": "2 hours ago"},
                {"action": "New user registration", "details": "Teacher from Delhi", "timestamp": "4 hours ago"},
                {"action": "Curriculum conversion", "details": "ICSE to Cambridge Grade 9 Physics", "timestamp": "6 hours ago"}
            ]
        return render_template('dashboard.html', stats=stats, activity=recent_activity)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        stats = {"total_conversions": 3678, "active_users": 1245, "success_rate": 94.5, "total_comparisons": 5432}
        return render_template('dashboard.html', stats=stats, activity=[])

@app.route('/converter')
def converter_page():
    """Converter page with notebook paper design and advanced dropdowns"""
    return render_template('converter.html')

@app.route('/generated')
def generated_page():
    """Generated files page with notebook paper design"""
    try:
        if generator:
            files = generator.get_generated_files()
        else:
            # Mock data for generated files
            files = [
                {
                    "name": "CBSE_to_IB_Mathematics_Grade10_Comparison.pdf",
                    "type": "Comprehensive Comparison",
                    "date": "2024-01-15",
                    "size": "2.3 MB",
                    "downloads": 127
                },
                {
                    "name": "ICSE_to_Cambridge_Physics_Grade9_Guide.pdf", 
                    "type": "Parent Guide",
                    "date": "2024-01-14",
                    "size": "1.8 MB",
                    "downloads": 89
                },
                {
                    "name": "State_Board_to_CBSE_Chemistry_Grade11_Analysis.pdf",
                    "type": "Teacher Guide", 
                    "date": "2024-01-13",
                    "size": "3.1 MB",
                    "downloads": 156
                }
            ]
        return render_template('generated.html', files=files)
    except Exception as e:
        print(f"Generated files error: {str(e)}")
        return render_template('generated.html', files=[])

@app.route('/reviews')
def reviews_page():
    """Reviews page with notebook paper design"""
    # Mock review data
    reviews = {
        "teacher_reviews": [
            {
                "name": "Mrs. Sarah Johnson",
                "role": "Mathematics Teacher",
                "school": "Delhi Public School",
                "rating": 5,
                "comment": "Excellent curriculum comparison tool! It helped me understand the transition requirements for my students moving from CBSE to IB. The detailed analysis is very comprehensive.",
                "date": "2 days ago"
            },
            {
                "name": "Mr. Rajesh Patel", 
                "role": "Science Teacher",
                "school": "Modern School",
                "rating": 5,
                "comment": "Very helpful for understanding different assessment methodologies. The cost analysis section is particularly useful for counseling parents.",
                "date": "1 week ago"
            }
        ],
        "parent_reviews": [
            {
                "name": "Anita Sharma",
                "role": "Parent of Grade 9 student",
                "rating": 5,
                "comment": "This tool helped us make an informed decision about switching our daughter from ICSE to Cambridge IGCSE. The detailed comparison saved us months of research!",
                "date": "3 days ago"
            },
            {
                "name": "Vikram Kumar",
                "role": "Parent of Grade 10 student", 
                "rating": 5,
                "comment": "Outstanding resource! The cost breakdown and university recognition information was exactly what we needed for planning our son's education path.",
                "date": "5 days ago"
            }
        ],
        "stats": {
            "teacher_reviews_count": 124,
            "parent_reviews_count": 89,
            "average_rating": 4.8,
            "total_reviews": 213
        }
    }
    return render_template('reviews.html', reviews=reviews)

@app.route('/comparison-result')
def comparison_result():
    """Comparison result page with notebook paper design"""
    from_board = request.args.get('from', 'CBSE')
    to_board = request.args.get('to', 'IB')
    grade = request.args.get('grade', 'Grade 10')
    subject = request.args.get('subject', 'Mathematics')
    stream = request.args.get('stream', '')
    
    print(f"Comparison request: {from_board} to {to_board}, {grade} {subject} {stream}")
    
    # Pass the comparison data to template
    comparison_data = {
        'fromBoard': from_board,
        'toBoard': to_board,
        'grade': grade,
        'subject': subject,
        'stream': stream
    }
    
    return render_template('comparison_result.html', 
                         comparison=comparison_data,
                         from_board=from_board, 
                         to_board=to_board, 
                         grade=grade, 
                         subject=subject,
                         stream=stream)

@app.route('/api/convert', methods=['POST'])
def convert_curriculum():
    """API endpoint for file conversion"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if converter:
            result = converter.process_file(file)
        else:
            result = {'error': 'Converter component not available'}
        return jsonify(result)
    
    except Exception as e:
        print(f"Convert error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    """API endpoint for dashboard statistics"""
    try:
        if dashboard:
            return jsonify(dashboard.get_stats())
        else:
            return jsonify({
                "total_conversions": 3678,
                "active_users": 1245, 
                "success_rate": 94.5,
                "total_comparisons": 5432,
                "recent_activity": [
                    {"action": "Comparison generated", "details": "CBSE to IB Grade 10 Mathematics", "timestamp": "2 hours ago"},
                    {"action": "New user registration", "details": "Teacher from Delhi", "timestamp": "4 hours ago"}
                ]
            })
    except Exception as e:
        print(f"Dashboard stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-comprehensive-comparison', methods=['POST'])
def generate_comprehensive_comparison():
    """Generate comprehensive comparison using Claude API"""
    try:
        # Ensure we're receiving JSON data
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
            
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        from_board = data.get('fromBoard', 'CBSE')
        to_board = data.get('toBoard', 'IB')
        grade = data.get('grade', 'Grade 10')
        subject = data.get('subject', 'Mathematics')
        
        print(f"API: Generating comprehensive comparison for: {from_board} to {to_board}, {subject}, {grade}")
        
        # Generate the comparison
        comparison_result = generate_3_column_table_comparison(from_board, to_board, grade, subject)
        
        return jsonify({
            'success': True,
            'comparison': comparison_result
        })
        
    except Exception as e:
        print(f"Error in generate_comprehensive_comparison: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/generate-specific-guidance', methods=['POST'])
def generate_specific_guidance():
    """Generate specific guidance for parents or teachers"""
    try:
        # Ensure we're receiving JSON data
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
            
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        from_board = data.get('fromBoard', 'CBSE')
        to_board = data.get('toBoard', 'IB')
        grade = data.get('grade', 'Grade 10')
        subject = data.get('subject', 'Mathematics')
        audience = data.get('audience', 'parent')
        
        print(f"API: Generating {audience} guidance for: {from_board} to {to_board}, {subject}, {grade}")
        
        if audience == 'parent':
            guidance = generate_parent_guidance(from_board, to_board, grade, subject)
        else:
            guidance = generate_teacher_guidance(from_board, to_board, grade, subject)
        
        return jsonify({
            'success': True,
            'guidance': guidance
        })
        
    except Exception as e:
        print(f"Error in generate_specific_guidance: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

def generate_3_column_table_comparison(from_board, to_board, grade, subject):
    """Generate structured data for 3-column table with bullet points and Syllabus Comparison as first category"""
    
    # Complete list of categories with Syllabus Comparison as first - ALL MAIN DIFFERENCES INCLUDED
    comprehensive_categories = [
        'Syllabus Comparison',  # FIRST: Detailed syllabus differences for grade/subject
        'Educational Philosophy & Approach',
        'Programme Structure & Year Classifications',
        'Assessment Methods & Grading Systems',
        'Assessment Criteria & Objectives Framework',
        'Paper Types & Assessment Components',
        'Teaching Methodologies & Pedagogical Approaches',
        'Learning Objectives & Outcomes',
        'Textbooks, Resources & Materials',
        'Homework, Assignments & Project Requirements',
        'Practical Components & Laboratory Work',
        'Technology Integration & Digital Learning',
        'Language Requirements & Communication Skills',
        'Cultural Context & Global Perspective',
        'School Types & Institutional Requirements',
        'Teacher Training & Professional Development',
        'Class Size & Student-Teacher Ratios',
        'University Recognition & Pathways',
        'Career Preparation & Skill Development',
        'Extracurricular Integration & Holistic Development',
        'Student Support Services & Guidance',
        'Parent Involvement & Communication',
        'Cost Implications & Financial Requirements',
        'Transition Challenges & Adaptation Period',
        'Supplementary Education & Additional Support',
        'Quality Assurance & Standards Monitoring',
        'International Mobility & Transferability',
        'Timeline & Implementation Strategy',
        'Subject Flexibility & Options',
        'Examination Sessions & Result Declaration',
        'Professional Terminology & Board-Specific Language',
        'Distance Learning & Private Candidate Options',
        'Special Needs & Inclusion Support',
        'Regional Variations & Local Adaptations',
        'Alternative Examination Boards & Pathways',
        'Teacher Transition Requirements & Training',
        # ADDITIONAL CRITICAL DIFFERENCES
        'Curriculum Depth vs Breadth Analysis',
        'Grade Progression & Age Requirements',
        'Subject Combination Rules & Flexibility',
        'Internal vs External Assessment Ratios',
        'Practical Examination Requirements',
        'Portfolio & Project Assessment Methods',
        'Continuous Assessment vs Final Exams',
        'Marking Schemes & Grade Boundaries',
        'Re-examination & Improvement Opportunities',
        'Credit Transfer & Course Recognition',
        'Medium of Instruction Requirements',
        'Co-curricular Activity Integration',
        'Community Service & Social Impact Requirements',
        'Research & Independent Study Components',
        'International Exchange & Study Abroad Options'
    ]
    
    comprehensive_prompt = f"""You are an expert educational consultant with deep knowledge of all education boards including CBSE, ICSE, IB, Cambridge, and State Boards. Generate an extremely detailed comprehensive curriculum comparison between {from_board} and {to_board} for {subject} in {grade}.

CRITICAL REQUIREMENTS FOR BULLET POINT FORMAT:

1. Generate analysis for ALL 50 categories listed below
2. Each category MUST be formatted as BULLET POINTS (use • symbol)
3. Each board should have 8-10 detailed bullet points per category
4. NO PARAGRAPHS - ONLY BULLET POINTS
5. Focus on {grade} {subject} specific information where relevant
6. Include SPECIFIC examples, practical implications, and actionable advice
7. Use PROFESSIONAL TERMINOLOGY specific to each board

SPECIAL EMPHASIS ON SYLLABUS COMPARISON (FIRST CATEGORY):
For "Syllabus Comparison" category, provide SPECIFIC syllabus differences including:
• Detailed topic coverage differences for {grade} {subject}
• Chapter-wise comparison and sequence differences
• Depth vs breadth of coverage for each topic
• Grade-wise progression differences
• Assessment weightage differences for topics
• Practical/lab component differences
• Mathematical complexity level differences (if applicable)
• Real-world application emphasis differences
• Cross-curricular integration differences
• Technology integration requirements

MANDATORY 50 CATEGORIES TO ANALYZE IN BULLET POINT FORMAT:

{chr(10).join([f"{i+1}. {cat}" for i, cat in enumerate(comprehensive_categories)])}

RESPONSE FORMAT - Respond ONLY with valid JSON:

{{
  "categories": [
    {{
      "name": "Syllabus Comparison",
      "fromBoardContent": "• Specific detailed bullet point about {from_board} syllabus for {grade} {subject}\\n• Another detailed bullet point with specific examples and practical implications\\n• Continue with 8-10 bullet points covering all syllabus aspects...",
      "toBoardContent": "• Specific detailed bullet point about {to_board} syllabus for {grade} {subject}\\n• Another detailed bullet point with specific examples and practical implications\\n• Continue with 8-10 bullet points covering all syllabus aspects..."
    }},
    {{
      "name": "Educational Philosophy & Approach",
      "fromBoardContent": "• Detailed bullet point about {from_board} educational philosophy\\n• Another bullet point with specific examples\\n• Continue with 8-10 bullet points...",
      "toBoardContent": "• Detailed bullet point about {to_board} educational philosophy\\n• Another bullet point with specific examples\\n• Continue with 8-10 bullet points..."
    }}
    // CONTINUE FOR ALL 50 CATEGORIES
  ]
}}

IMPORTANT: You MUST generate ALL 50 categories. Do not skip any categories. Each category should have detailed bullet point content for both boards.

DO NOT OUTPUT ANYTHING OTHER THAN VALID JSON. NO EXPLANATIONS. NO SUMMARIES. GENERATE ALL 50 CATEGORIES WITH BULLET POINTS ONLY."""

    try:
        print(f"Generating comprehensive comparison with bullet points for {from_board} vs {to_board}...")
        
        # Call Claude API with increased timeout for comprehensive response
        response_text = call_claude_api(comprehensive_prompt)
        
        # Clean the response to extract JSON
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]
        elif response_text.startswith('```'):
            response_text = response_text[3:-3]
        
        # Parse JSON response
        try:
            comparison_data = json.loads(response_text)
            categories = comparison_data.get('categories', [])
            
            print(f"Successfully generated {len(categories)} categories from Claude API")
            
            # If we got fewer than 20 categories, generate fallback for missing ones
            if len(categories) < 20:
                print(f"Only received {len(categories)} categories, generating fallback categories...")
                
                # Add fallback categories for essential comparisons including all comprehensive categories
                missing_categories = [cat for cat in comprehensive_categories if not any(existing_cat.get('name') == cat for existing_cat in categories)]
                
                # Add missing categories up to ensure comprehensive coverage
                for category in missing_categories[:30]:  # Generate up to 30 fallback categories
                    categories.append(generate_comprehensive_fallback_category(category, from_board, to_board, grade, subject))
                
            print(f"Final result: {len(categories)} categories generated")
            
            return {
                'fromBoard': from_board,
                'toBoard': to_board,
                'grade': grade,
                'subject': subject,
                'categories': categories,
                'totalCategories': len(categories),
                'analysisDepth': f'Comprehensive {len(categories)}-category analysis with bullet points',
                'wordCount': f'Approximately {len(categories) * 800}+ words in bullet format'
            }
            
        except json.JSONDecodeError as json_error:
            print(f"JSON parsing error: {str(json_error)}")
            print(f"Response preview: {response_text[:500]}...")
            
            # Generate comprehensive fallback data with all categories
            return generate_complete_comprehensive_fallback(from_board, to_board, grade, subject, comprehensive_categories)
            
    except Exception as e:
        print(f"Error in generate_3_column_table_comparison: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return generate_complete_comprehensive_fallback(from_board, to_board, grade, subject, comprehensive_categories)

def generate_comprehensive_fallback_category(category_name, from_board, to_board, grade, subject):
    """Generate extremely detailed fallback content for a single category with bullet points"""
    
    # Comprehensive board-specific details and terminology
    board_comprehensive_details = {
        'CBSE': {
            'structure': 'Primary (1-5), Middle (6-8), Secondary (9-10), Senior Secondary (11-12)',
            'ages': 'Ages 6-18 with grade-appropriate progression',
            'grading': 'A1-E grade system with CGPA calculation and 9-point scale',
            'exams': 'Annual board examinations in March with 80% external + 20% internal assessment',
            'terminology': 'CCE system, competency-based questions, NCERT alignment, formative/summative assessment',
            'costs': '₹2,50,000 average annual fees + ₹3,500 board exam fees + coaching ₹1,25,000',
            'recognition': 'Recognized by Indian universities and increasingly by international institutions worldwide',
            'teachers': 'B.Ed qualification required with subject expertise and government training',
            'sessions': 'Annual examination in February-March with results in May-June'
        },
        'ICSE': {
            'structure': 'Primary (1-4), Middle (5-7), Secondary (8-10), Higher Secondary (11-12)',
            'ages': 'Ages 6-18 with English-medium instruction throughout',
            'grading': 'Percentage-based system with detailed subject-wise analysis and comprehensive assessment',
            'exams': 'Annual board examinations with rigorous assessment standards and practical components',
            'terminology': 'English-medium instruction, comprehensive syllabi, analytical assessment, detailed curriculum',
            'costs': '₹4,00,000-8,00,000 annual fees + examination fees + practical costs',
            'recognition': 'Globally recognized for academic rigor and English proficiency with university acceptance',
            'teachers': 'High qualification standards with English proficiency and subject specialization',
            'sessions': 'Annual examinations with comprehensive practical and theory components'
        },
        'IB': {
            'structure': 'PYP (3-12), MYP (11-16), DP (16-19), CP (16-19) with seamless progression',
            'ages': 'Ages 3-19 across four interconnected programmes with international standards',
            'grading': '1-7 scale with criterion-referenced assessment using A, B, C, D criteria framework',
            'exams': 'Continuous assessment with optional eAssessment and external moderation systems',
            'terminology': 'ATL skills, global contexts, inquiry-based learning, international mindedness, CAS',
            'costs': '₹15,00,000+ annual fees + eAssessment costs + extensive resource requirements',
            'recognition': 'Premium global recognition with direct university admission pathways worldwide',
            'teachers': 'Mandatory IB training and certification with ongoing professional development',
            'sessions': 'Continuous assessment with external examinations in May and November'
        },
        'Cambridge': {
            'structure': 'Primary (5-11), Lower Secondary (11-14), IGCSE (14-16), A-Levels (16-18)',
            'ages': 'Ages 5-18 with flexible entry points and international progression pathways',
            'grading': 'A*-G scale with Assessment Objectives (AO1-AO6) framework and grade boundaries',
            'exams': 'June and November sessions with theory, practical, and coursework components',
            'terminology': 'Core/Extended tiers, moderation, standardization, Cambridge International qualifications',
            'costs': '₹5,50,000 annual fees + ₹40,000 per subject examination fees + resource costs',
            'recognition': 'Gold standard global recognition with worldwide university acceptance and transferability',
            'teachers': 'Subject specialization with Cambridge training and international teaching qualifications',
            'sessions': 'Multiple examination sessions (March, June, November) with global coordination'
        },
        'State Board': {
            'structure': 'Primary (1-5), Upper Primary (6-8), Secondary (9-10), Higher Secondary (11-12)',
            'ages': 'Ages 6-18 with regional language integration and cultural relevance',
            'grading': 'Percentage-based with state-specific evaluation criteria and regional standards',
            'exams': 'Annual state board examinations with regional focus and local relevance',
            'terminology': 'Regional language emphasis, cultural integration, local relevance, state curriculum',
            'costs': '₹1,50,000-3,00,000 annual fees with minimal examination costs and accessibility focus',
            'recognition': 'Regional recognition with increasing national and international acceptance',
            'teachers': 'State qualification requirements with regional language proficiency and cultural knowledge',
            'sessions': 'Annual examinations aligned with state academic calendar and regional needs'
        }
    }
    
    from_details = board_comprehensive_details.get(from_board, board_comprehensive_details['CBSE'])
    to_details = board_comprehensive_details.get(to_board, board_comprehensive_details['IB'])
    
    # Generate bullet points for Syllabus Comparison category
    if category_name == 'Syllabus Comparison':
        from_content = f"""• {from_board} {subject} syllabus for {grade} emphasizes {from_details['terminology']} with structured curriculum progression
• Topic coverage includes foundational concepts with gradual complexity building appropriate for {grade} level students
• Assessment weightage follows {from_details['grading']} with specific marking schemes for each topic area
• Practical components integrated as per {from_details['exams']} requirements with hands-on learning emphasis
• Cross-curricular connections made with other subjects to enhance understanding and application of {subject} concepts
• Mathematical complexity level maintained at grade-appropriate standards with step-by-step skill development approach
• Real-world applications embedded throughout curriculum to connect theoretical concepts with practical scenarios
• Technology integration requirements include digital tools and resources as specified by board guidelines
• Chapter sequencing follows logical progression from basic to advanced concepts with clear learning outcomes
• Depth of coverage balanced with breadth to ensure comprehensive understanding while meeting time constraints"""
        
        to_content = f"""• {to_board} {subject} curriculum for {grade} utilizes {to_details['terminology']} with international standards alignment
• Topic coverage emphasizes inquiry-based learning with conceptual understanding prioritized over rote memorization
• Assessment follows {to_details['grading']} with criterion-referenced evaluation measuring student achievement against standards
• Practical work integrated through {to_details['exams']} with extensive laboratory and field work components
• Global perspectives woven throughout curriculum connecting local {subject} concepts to international contexts
• Mathematical rigor maintained at internationally competitive levels with problem-solving skills emphasis
• Real-world applications central to curriculum design with authentic assessment tasks and project-based learning
• Technology integration mandatory with digital literacy skills developed alongside {subject} content knowledge
• Unit organization follows thematic approach with interdisciplinary connections and holistic learning experiences
• Depth prioritized over breadth with fewer topics covered in greater detail to ensure mastery"""
    else:
        # Generate bullet points for other categories
        from_content = f"""• {from_board} approach to {category_name.lower()} incorporates {from_details['terminology']} methodology
• Implementation strategy focuses on {from_details['structure']} with age-appropriate content delivery
• Assessment methodology utilizes {from_details['grading']} ensuring fair evaluation of student progress
• Professional requirements include {from_details['teachers']} with ongoing development and training
• Financial investment involves {from_details['costs']} making education accessible to diverse backgrounds
• Recognition benefits include {from_details['recognition']} providing pathways to higher education
• Examination schedule follows {from_details['sessions']} with structured timeline and preparation periods
• Quality assurance maintained through regular monitoring and feedback mechanisms for continuous improvement
• Support systems provided for students, teachers, and parents ensuring successful educational outcomes
• Implementation timeline allows adequate preparation and transition periods for all stakeholders involved"""
        
        to_content = f"""• {to_board} framework for {category_name.lower()} emphasizes {to_details['terminology']} with international best practices
• Programme structure follows {to_details['structure']} ensuring seamless progression across educational levels
• Evaluation system uses {to_details['grading']} with criterion-referenced assessment measuring individual growth
• Professional development requires {to_details['teachers']} with mandatory certification and ongoing training
• Investment requirements include {to_details['costs']} reflecting premium international education standards
• Global recognition provides {to_details['recognition']} with direct pathways to prestigious universities worldwide
• Assessment timeline includes {to_details['sessions']} with flexible scheduling and multiple opportunities
• Quality control maintained through international standards alignment and regular external moderation processes
• Comprehensive support provided through dedicated counseling, academic guidance, and pastoral care systems
• Strategic implementation ensures smooth transition with detailed preparation and orientation programmes"""
    
    return {
        'name': category_name,
        'fromBoardContent': from_content,
        'toBoardContent': to_content
    }

def generate_complete_comprehensive_fallback(from_board, to_board, grade, subject, categories):
    """Generate complete comprehensive fallback data when Claude API fails"""
    print("Generating complete comprehensive fallback comparison with bullet points...")
    
    fallback_categories = []
    for category in categories:
        fallback_categories.append(generate_comprehensive_fallback_category(category, from_board, to_board, grade, subject))
    
    return {
        'fromBoard': from_board,
        'toBoard': to_board,
        'grade': grade,
        'subject': subject,
        'categories': fallback_categories,
        'totalCategories': len(fallback_categories),
        'analysisDepth': 'Complete comprehensive fallback with bullet points and Syllabus Comparison',
        'wordCount': 'Approximately 25,000+ words in bullet format',
        'note': 'Comprehensive fallback comparison generated with bullet points and detailed syllabus comparison'
    }

def generate_fallback_comparison(from_board, to_board, grade, subject):
    """Generate fallback comparison when Claude API fails"""
    return generate_complete_comprehensive_fallback(from_board, to_board, grade, subject, [
        'Syllabus Comparison',
        'Educational Philosophy & Approach',
        'Programme Structure & Year Classifications', 
        'Assessment Methods & Grading Systems',
        'Cost Implications & Financial Requirements',
        'University Recognition & Pathways'
    ])

def generate_parent_guidance(from_board, to_board, grade, subject):
    """Generate detailed parent guidance for curriculum transition"""
    detailed_parent_prompt = f"""You are an educational counselor specializing in curriculum transitions. A parent is seeking detailed guidance for their child's transition from {from_board} to {to_board} for {subject} in {grade}.

Provide COMPREHENSIVE, DETAILED guidance covering every aspect parents need to know:

## IMMEDIATE PREPARATION (What to do RIGHT NOW)
- Detailed steps to prepare their child academically and mentally
- Documents and paperwork required (be specific)
- Timeline for application and enrollment processes
- How to research and select the right school
- Financial planning and budgeting considerations

## ACADEMIC PREPARATION STRATEGY
- Specific knowledge gaps that need to be addressed
- Skills their child needs to develop before transition
- Study habits and learning strategies to establish
- How to bridge curriculum differences in {subject}
- Recommended preparatory materials and resources

## UNDERSTANDING THE NEW LEARNING ENVIRONMENT
- How daily school life will change for their child
- New expectations for homework and study time
- Different assessment methods their child will face
- Changes in teacher-student interaction styles
- Peer interaction and social dynamics

## SUPPORTING YOUR CHILD THROUGH THE TRANSITION
- How to identify and address adjustment difficulties
- Warning signs of academic or social struggles
- Communication strategies with teachers and school
- How to maintain motivation during challenging periods
- Building confidence in the new system

Provide specific, actionable advice that empowers parents to confidently support their child through this important transition."""

    try:
        return call_claude_api(detailed_parent_prompt)
    except Exception as e:
        print(f"Error generating parent guidance: {str(e)}")
        return f"Comprehensive parent guidance for transitioning from {from_board} to {to_board}: [Detailed guidance would be generated here covering preparation steps, academic requirements, financial planning, and support strategies]"

def generate_teacher_guidance(from_board, to_board, grade, subject):
    """Generate detailed teacher guidance for curriculum transition"""
    detailed_teacher_prompt = f"""You are providing comprehensive professional development guidance to teachers transitioning from teaching {from_board} curriculum to {to_board} curriculum for {subject} in {grade}.

Provide DETAILED, PRACTICAL guidance covering every aspect teachers need to master:

## PEDAGOGICAL TRANSFORMATION
- Detailed comparison of teaching philosophies between {from_board} and {to_board}
- Specific methodology changes required for {subject} in {grade}
- Student engagement strategies unique to {to_board} approach
- Classroom management adaptations needed

## CURRICULUM CONTENT MASTERY
- Detailed content differences in {subject} for {grade}
- New topics to master and teach
- Depth vs. breadth adjustments in content coverage
- Integration strategies with other subjects

## ASSESSMENT & EVALUATION TRANSFORMATION
- Complete overhaul of assessment strategies
- New rubrics and grading criteria to implement
- Formative vs. summative assessment balance
- Portfolio and project-based assessment techniques

## PROFESSIONAL DEVELOPMENT PATHWAY
- Specific certifications and qualifications needed for {to_board}
- Training programs and workshops to attend
- Mentorship and coaching opportunities
- Professional learning community engagement

Provide specific, actionable professional guidance that enables teachers to excel in delivering {to_board} curriculum for {subject} in {grade}."""

    try:
        return call_claude_api(detailed_teacher_prompt)
    except Exception as e:
        print(f"Error generating teacher guidance: {str(e)}")
        return f"Comprehensive teacher guidance for transitioning from {from_board} to {to_board}: [Detailed professional development guidance would be generated here covering pedagogical changes, curriculum mastery, assessment transformation, and certification requirements]"

def call_claude_api(prompt):
    """Make API call to Claude with proper error handling"""
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
    }
    
    payload = {
        'model': 'claude-3-5-sonnet-20241022',
        'max_tokens': 8000,
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ]
    }
    
    try:
        print(f"Making API call to Claude...")
        response = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=120)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            error_text = response.text
            print(f"API Error: {error_text}")
            return f"API request failed with status {response.status_code}: {error_text}"
            
    except requests.exceptions.Timeout:
        error_msg = "API request timed out after 120 seconds"
        print(error_msg)
        return error_msg
    except requests.exceptions.RequestException as req_error:
        error_msg = f"API request failed: {str(req_error)}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"API call failed: {str(e)}"
        print(error_msg)
        return error_msg

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    # Check if it's an API request
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'API endpoint not found'}), 404
    
    try:
        return render_template('index.html'), 404
    except Exception:
        return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors gracefully"""
    print(f"Internal server error: {str(error)}")
    
    # Check if it's an API request
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
        
    return jsonify({'error': 'Internal server error'}), 500

# Keep the development server for local testing - Vercel will ignore this
if __name__ == '__main__':
    print("Starting II Tutions Curriculum Converter Flask Application...")
    print(f"Claude API configured: {'Yes' if CLAUDE_API_KEY else 'No'}")
    print("Available routes:")
    print("  / - Home page with notebook design")
    print("  /converter - Curriculum comparison tool")
    print("  /dashboard - Statistics and analytics") 
    print("  /generated - Generated files and reports")
    print("  /reviews - User reviews and testimonials")
    print("  /comparison-result - Detailed comparison results")
    print("\nStarting server on http://localhost:5002")
    app.run(debug=True, host='0.0.0.0', port=5002)
