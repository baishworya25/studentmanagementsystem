import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ------------------ BASE CLASS (OOP ) ------------------
class User:
    """Base class for all users - Demonstrates Inheritance"""
    
    def __init__(self, username):
        self.username = username
        self.data_dir = 'data/'
        self.user_id = None
        self.name = None
        self.email = None
        self.role = None
        self.load_user_info()

    def load_user_info(self):
        """Load user info from users.txt with exception handling"""
        try:
            users_file = self.data_dir + 'users.txt'
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    for line in f:
                        data = line.strip().split(',')
                        if len(data) >= 5 and data[1] == self.username:
                            self.user_id = data[0]
                            self.name = data[2]
                            self.email = data[3]
                            self.role = data[4].strip()
                            return
        except Exception as e:
            print(f" Error loading user info: {e}")

# ------------------ STUDENT CLASS  ------------------
class Student(User):
    """Student class - Inherits from User"""
    
    def view_profile(self):
        """View personal details, grades, ECA"""
        print(f"\n PERSONAL PROFILE ({self.user_id})")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Role: {self.role}")
        self.view_grades()
        self.view_eca()

    def update_profile(self):
        """Update profile information"""
        try:
            print(f"\nCurrent: {self.name} ({self.email})")
            new_name = input("New name (Enter to keep): ").strip()
            new_email = input("New email (Enter to keep): ").strip()

            if new_name: self.name = new_name
            if new_email: self.email = new_email

            self.save_user_info()
            print(" Profile updated successfully!")
        except Exception as e:
            print(f" Update error: {e}")

    def save_user_info(self):
        """Save to users.txt"""
        try:
            users_file = self.data_dir + 'users.txt'
            lines = []
            
            if os.path.exists(users_file):
                with open(users_file, 'r') as f:
                    lines = f.readlines()
            
            with open(users_file, 'w') as f:
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) >= 5 and data[1] == self.username:
                        f.write(f"{self.user_id},{self.username},{self.name},{self.email},{self.role}\n")
                    else:
                        f.write(line)
        except Exception as e:
            print(f" Save error: {e}")

    def view_grades(self):
        """View exam grades for 5 subjects"""
        try:
            grades_file = self.data_dir + 'grades.txt'
            if os.path.exists(grades_file):
                with open(grades_file, 'r') as f:
                    for line in f:
                        data = line.strip().split(',')
                        if data[0] == self.user_id:
                            subjects = ['FODS', 'IT', 'English', 'Multimedia', 'CS']
                            print("\n EXAM GRADES:")
                            total = 0
                            count = 0
                            for i, grade in enumerate(data[1:6]):
                                print(f"  {subjects[i]}: {grade}")
                                try:
                                    total += float(grade)
                                    count += 1
                                except:
                                    pass
                            if count > 0:
                                print(f"   Average: {total/count:.1f}%")
                            return
            print(" No grades found!")
        except Exception as e:
            print(f" Grades error: {e}")

    def view_eca(self):
        """View extracurricular activities"""
        try:
            eca_file = self.data_dir + 'eca.txt'
            if os.path.exists(eca_file):
                with open(eca_file, 'r') as f:
                    for line in f:
                        data = line.strip().split(',')
                        if data[0] == self.user_id:
                            activities = [x.strip() for x in data[1:] if x.strip()]
                            print(f"\n ECA ACTIVITIES ({len(activities)}):")
                            if activities:
                                for activity in activities:
                                    print(f"  • {activity}")
                            else:
                                print("  None")
                            return
            print(" No ECA records!")
        except Exception as e:
            print(f" ECA error: {e}")

    def view_grades_chart(self):
        """BONUS: Visualize grades (Creativity 10pts)"""
        try:
            grades_file = self.data_dir + 'grades.txt'
            grades = []
            if os.path.exists(grades_file):
                with open(grades_file, 'r') as f:
                    for line in f:
                        data = line.strip().split(',')
                        if data[0] == self.user_id:
                            grades = [float(x) for x in data[1:6]]
                            break
            
            if grades:
                subjects = ['FODS', 'IT', 'English', 'Multimedia', 'CS']
                plt.figure(figsize=(10, 6))
                plt.bar(subjects, grades, color=['#FF6B6B', '#4ECDC4', '#45B7D1', "#96CEB4", '#FFEAA7'])
                plt.title(f" {self.name}'s Grades", fontsize=16)
                plt.ylabel('Marks', fontsize=12)
                plt.ylim(0, 100)
                plt.grid(axis='y', alpha=0.3)
                for i, v in enumerate(grades):
                    plt.text(i, v + 1, f'{v:.0f}', ha='center', fontweight='bold')
                plt.tight_layout()
                plt.show()
                print(" Chart displayed!")
            else:
                print(" No grades data for chart!")
        except Exception as e:
            print(f" Chart error: {e}")

# ------------------ ADMIN CLASS (Requirement 2) ------------------
class Admin(User):
    """Admin class with full CRUD operations"""
    
    def add_user(self):
        """Add new users with UNIQUE IDs (auto-generated)"""
        try:
            print("\n ADD NEW USER")
            role = input("Role (student/admin): ").strip().lower()
            username = input("Username: ").strip()
            name = input("Full Name: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            # AUTO-GENERATE UNIQUE ID
            user_id = self.generate_unique_id(role)
            
            # Validate uniqueness
            if self.username_exists(username):
                print(" Username already exists!")
                return
            
            # Save to users.txt
            with open(self.data_dir + 'users.txt', 'a') as f:
                f.write(f"{user_id},{username},{name},{email},{role}\n")
            
            # Save to passwords.txt
            with open(self.data_dir + 'passwords.txt', 'a') as f:
                f.write(f"{username},{password}\n")
            
            # Initialize student records
            if role == 'student':
                with open(self.data_dir + 'grades.txt', 'a') as f:
                    f.write(f"{user_id},0,0,0,0,0\n")
                with open(self.data_dir + 'eca.txt', 'a') as f:
                    f.write(f"{user_id},\n")
            
            print(f" New {role.upper()} added! ID: {user_id}")
        except Exception as e:
            print(f" Add user error: {e}")

    def generate_unique_id(self, role):
        """Generate unique ID: STU001, ADM001 format"""
        prefix = 'STU' if role == 'student' else 'ADM'
        count = 1
        try:
            with open(self.data_dir + 'users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0].startswith(prefix):
                        count += 1
        except:
            pass
        return f"{prefix}{count:03d}"

    def username_exists(self, username):
        """Check username uniqueness"""
        try:
            with open(self.data_dir + 'passwords.txt', 'r') as f:
                for line in f:
                    if line.strip().split(',')[0] == username:
                        return True
        except:
            pass
        return False

    def modify_student_record(self):
        """Update personal, grades, ECA records"""
        student_id = input("Enter Student ID: ").strip()
        if not self.student_exists(student_id):
            print(" Student not found!")
            return
        
        print("\n1. Personal Info  2. Grades  3. ECA")
        choice = input("Choice: ").strip()
        
        if choice == '1':
            self.update_personal_info(student_id)
        elif choice == '2':
            self.update_grades(student_id)
        elif choice == '3':
            self.update_eca(student_id)

    def student_exists(self, student_id):
        """Check if student exists"""
        try:
            with open(self.data_dir + 'users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0] == student_id and data[4] == 'student':
                        return True
        except:
            pass
        return False

    def update_personal_info(self, student_id):
        """Update student personal info"""
        try:
            lines = []
            with open(self.data_dir + 'users.txt', 'r') as f:
                lines = f.readlines()
            
            with open(self.data_dir + 'users.txt', 'w') as f:
                for line in lines:
                    data = line.strip().split(',')
                    if data[0] == student_id:
                        print(f"Current: {data[2]} ({data[3]})")
                        data[2] = input("New name: ").strip() or data[2]
                        data[3] = input("New email: ").strip() or data[3]
                        f.write(','.join(data) + '\n')
                    else:
                        f.write(line)
            print(" Personal info updated!")
        except Exception as e:
            print(f" Update error: {e}")

    def update_grades(self, student_id):
        """Update exam grades"""
        try:
            print("Enter 5 grades (FODS, IT, English, Multimedia, CS):")
            grades = input("Grades (space separated): ").strip().split()
            if len(grades) != 5:
                print(" Need exactly 5 grades!")
                return
            
            lines = []
            with open(self.data_dir + 'grades.txt', 'r') as f:
                lines = f.readlines()
            
            with open(self.data_dir + 'grades.txt', 'w') as f:
                found = False
                for line in lines:
                    data = line.strip().split(',')
                    if data[0] == student_id:
                        f.write(f"{student_id},{','.join(grades)}\n")
                        found = True
                    else:
                        f.write(line)
                if not found:
                    f.write(f"{student_id},{','.join(grades)}\n")
            print(" Grades updated!")
        except Exception as e:
            print(f" Grades error: {e}")

    def update_eca(self, student_id):
        """Update ECA activities"""
        try:
            new_eca = input("ECA activities (space separated): ").strip().split()
            lines = []
            with open(self.data_dir + 'eca.txt', 'r') as f:
                lines = f.readlines()
            
            with open(self.data_dir + 'eca.txt', 'w') as f:
                found = False
                for line in lines:
                    data = line.strip().split(',')
                    if data[0] == student_id:
                        f.write(f"{student_id},{','.join(new_eca)}\n")
                        found = True
                    else:
                        f.write(line)
                if not found:
                    f.write(f"{student_id},{','.join(new_eca)}\n")
            print(" ECA updated!")
        except Exception as e:
            print(f" ECA error: {e}")

    def delete_student(self):
        """Delete complete student record"""
        student_id = input("Student ID to delete: ").strip()
        if not self.student_exists(student_id):
            print(" Student not found!")
            return
        
        confirm = input(f"Delete {student_id} from ALL files? (y/N): ").strip().lower()
        if confirm != 'y':
            print(" Cancelled!")
            return
        
        # Get username first
        username = None
        try:
            with open(self.data_dir + 'users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if data[0] == student_id:
                        username = data[1]
                        break
        except:
            pass
        
        # Delete from all files
        files = ['users.txt', 'grades.txt', 'eca.txt']
        for filename in files:
            self.remove_line(filename, student_id)
        
        if username:
            self.remove_line('passwords.txt', username, is_username=True)
        
        print(" Student completely deleted!")

    def remove_line(self, filename, key, is_username=False):
        """Remove line from file"""
        try:
            lines = []
            filepath = self.data_dir + filename
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            with open(filepath, 'w') as f:
                for line in lines:
                    data = line.strip().split(',')
                    if is_username:
                        if len(data) > 0 and data[0] != key:
                            f.write(line)
                    else:
                        if not line.strip().startswith(key + ','):
                            f.write(line)
        except Exception as e:
            print(f" Delete error in {filename}: {e}")

    def view_all_students(self):
        """View all students"""
        try:
            print("\n ALL STUDENTS")
            print("ID\t\tName\t\tUsername\tEmail")
            print("-" * 50)
            with open(self.data_dir + 'users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 5 and data[4] == 'student':
                        print(f"{data[0]}\t\t{data[2]}\t\t{data[1]}\t\t{data[3]}")
        except Exception as e:
            print(f" View error: {e}")

    def generate_insights(self):
        """Generate useful insights (Requirement 2)"""
        try:
            print("\n DATA INSIGHTS")
            print("=" * 30)
            
            # 1. Average grades per subject
            subjects = ['FODS', 'IT', 'English', 'Multimedia', 'CS']
            totals = [0] * 5
            count = 0
            
            with open(self.data_dir + 'grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) > 5:
                        grades = [float(x) for x in data[1:6]]
                        totals = [a + b for a, b in zip(totals, grades)]
                        count += 1
            
            print(" AVERAGE GRADES PER SUBJECT:")
            for i, subject in enumerate(subjects):
                avg = totals[i] / count if count > 0 else 0
                print(f"  {subject}: {avg:.1f}%")
            
            # 2. Most active ECA students
            eca_count = {}
            with open(self.data_dir + 'eca.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) > 1:
                        eca_count[data[0]] = len(data) - 1
            
            if eca_count:
                most_active = max(eca_count.items(), key=lambda x: x[1])
                print(f"\n MOST ACTIVE ECA: {most_active[0]} ({most_active[1]} activities)")
            
            print(f"\n Total Students: {count}")
        except Exception as e:
            print(f" Insights error: {e}")

# ------------------ ANALYTICS DASHBOARD (task 2) ------------------
class AnalyticsDashboard:
    """Task 2: Performance Analytics Dashboard"""
    
    def __init__(self):
        self.data_dir = 'data/'
    
    def show_full_dashboard(self):
        """Complete analytics dashboard"""
        print("\n PERFORMANCE ANALYTICS DASHBOARD")
        print("1.  Grade Trends Chart")
        print("2.  ECA vs Performance Correlation")
        print("3.  Performance Alerts (<70%)")
        print("4.  Full Report")
        choice = input("Choice (1-4): ").strip()
        
        try:
            if choice == '1':
                self.grade_trends_chart()
            elif choice == '2':
                self.eca_correlation()
            elif choice == '3':
                self.performance_alerts()
            elif choice == '4':
                self.full_report()
        except Exception as e:
            print(f" Dashboard error: {e}")
            print(" Install: pip install pandas matplotlib numpy")

    def grade_trends_chart(self):
        """Grade trends visualization"""
        try:
            data = []
            names = []
            
            # Get student names
            name_map = {}
            with open(self.data_dir + 'users.txt', 'r') as f:
                for line in f:
                    data_user = line.strip().split(',')
                    if len(data_user) >= 5 and data_user[4] == 'student':
                        name_map[data_user[0]] = data_user[2]
            
            # Get grades
            with open(self.data_dir + 'grades.txt', 'r') as f:
                for line in f:
                    data_grade = line.strip().split(',')
                    sid = data_grade[0]
                    if sid in name_map and len(data_grade) >= 6:
                        try:
                            grades = [float(x) for x in data_grade[1:6]]
                            names.append(name_map[sid])
                            data.append(grades)
                        except:
                            pass
            
            if data:
                df = pd.DataFrame(data, index=names, 
                                columns=['FODS', 'IT', 'English', 'Multimedia', 'CS'])
                plt.figure(figsize=(12, 6))
                df.plot(kind='bar')
                plt.title(' Grade Trends - All Students', fontsize=16)
                plt.ylabel('Marks')
                plt.xlabel('Students')
                plt.xticks(rotation=45, ha='right')
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                plt.show()
                print(" Grade trends chart displayed!")
            else:
                print(" No grade data available!")
        except Exception as e:
            print(f" Chart error: {e}")

    def eca_correlation(self):
        """Correlate ECA involvement with performance"""
        try:
            grade_avgs = {}
            eca_counts = {}
            
            # Average grades
            with open(self.data_dir + 'grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 6:
                        try:
                            avg = sum(float(x) for x in data[1:6]) / 5
                            grade_avgs[data[0]] = avg
                        except:
                            pass
            
            # ECA counts
            with open(self.data_dir + 'eca.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) > 1:
                        count = len([x for x in data[1:] if x.strip()])
                        eca_counts[data[0]] = count
            
            # Common students
            common_ids = set(grade_avgs.keys()) & set(eca_counts.keys())
            if len(common_ids) < 2:
                print(" Insufficient data for correlation!")
                return
            
            x = [eca_counts[sid] for sid in common_ids]
            y = [grade_avgs[sid] for sid in common_ids]
            
            plt.figure(figsize=(10, 6))
            plt.scatter(x, y, s=100, alpha=0.7, color='coral')
            
            # Trend line
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x), "r--", linewidth=2, label=f'Correlation: {np.corrcoef(x, y)[0,1]:.2f}')
            
            plt.xlabel('Number of ECA Activities')
            plt.ylabel('Average Grade (%)')
            plt.title(' ECA Involvement vs Academic Performance')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()
            
            print(" ECA correlation chart displayed!")
        except Exception as e:
            print(f" Correlation error: {e}")

    def performance_alerts(self):
        """Identify students below threshold"""
        try:
            alerts = []
            name_map = {}
            
            # Student names
            with open(self.data_dir + 'users.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 5 and data[4] == 'student':
                        name_map[data[0]] = data[2]
            
            # Check grades
            with open(self.data_dir + 'grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    sid = data[0]
                    if sid in name_map and len(data) >= 6:
                        try:
                            avg = sum(float(x) for x in data[1:6]) / 5
                            if avg < 70:  # Threshold
                                alerts.append((name_map[sid], sid, avg))
                        except:
                            pass
            
            print("\n PERFORMANCE ALERTS (Average < 70%)")
            print("=" * 50)
            if alerts:
                for name, sid, avg in alerts:
                    print(f"  {name} (ID: {sid}) - {avg:.1f}%")
                    print("    Suggested interventions:")
                    print("      - Extra tutoring sessions")
                    print("      - Study skills workshop")
                    print("      - Parent-teacher meeting")
                    print()
                print(f" Total alerts: {len(alerts)} students")
            else:
                print(" All students above performance threshold!")
        except Exception as e:
            print(f" Alerts error: {e}")

    def full_report(self):
        """Complete analytics report"""
        try:
            print("\n COMPLETE PERFORMANCE REPORT")
            print("=" * 60)
            
            # Summary stats
            grade_data = []
            with open(self.data_dir + 'grades.txt', 'r') as f:
                for line in f:
                    data = line.strip().split(',')
                    if len(data) >= 6:
                        try:
                            grades = [float(x) for x in data[1:6]]
                            grade_data.append(grades)
                        except:
                            pass
            
            if grade_data:
                df = pd.DataFrame(grade_data, 
                                columns=['FODS', 'IT', 'English', 'Multimedia', 'CS'])
                print(" CLASS AVERAGES:")
                print(df.mean().round(1))
                print()
                
                # Top/Bottom performers
                avgs = df.mean(axis=1)
                print(" TOP PERFORMERS (Top 3):")
                top_indices = avgs.nlargest(3).index
                for i in top_indices:
                    print(f"  Student {i+1}: {avgs[i]:.1f}%")
                
                print("\n LOW PERFORMERS (Bottom 3):")
                bottom_indices = avgs.nsmallest(3).index
                for i in bottom_indices:
                    print(f"  Student {i+1}: {avgs[i]:.1f}%")
            
            print("\n Full report generated!")
        except Exception as e:
            print(f" Report error: {e}")


# Your original main.py expects Admin.dashboard
Admin.dashboard = AnalyticsDashboard()