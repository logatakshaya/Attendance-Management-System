import streamlit as st
from datetime import date

from database import (
    create_database,
    login_user,
    add_student,
    get_students,
    search_students,
    update_student,
    delete_student,
    save_attendance,
    get_attendance_by_date,
    get_attendance_records,
    get_student_attendance,
    get_student_attendance_summary
)

# ============================================================
# DATABASE
# ============================================================

create_database()

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Attendance Management System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>
.stApp {
background-color: #f5f7fb;
}

section[data-testid="stSidebar"] {
background-color: #ffffff;
border-right: 1px solid #e5e7eb;
}

.sidebar-title {
text-align: center;
font-size: 24px;
font-weight: 700;
color: #1e3a8a;
margin-bottom: 5px;
}

.sidebar-subtitle {
text-align: center;
font-size: 13px;
color: #64748b;
margin-bottom: 25px;
}

h1 {
color: #172554;
font-weight: 700;
}

h2 {
color: #1e3a8a;
}

h3 {
color: #1e40af;
}

.dashboard-card {
background-color: #ffffff;
padding: 22px;
border-radius: 14px;
border: 1px solid #e5e7eb;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
text-align: center;
margin-bottom: 15px;
}

.card-title {
color: #64748b;
font-size: 14px;
font-weight: 600;
margin-bottom: 8px;
}

.card-value {
color: #1e3a8a;
font-size: 30px;
font-weight: 700;
}

.welcome-banner {
background: linear-gradient(135deg, #1e3a8a, #2563eb);
color: white;
padding: 28px;
border-radius: 16px;
margin-bottom: 25px;
box-shadow: 0 4px 12px rgba(37, 99, 235, 0.20);
}

.welcome-title {
font-size: 28px;
font-weight: 700;
margin-bottom: 6px;
}

.welcome-text {
font-size: 15px;
opacity: 0.9;
}

.login-title {
text-align: center;
color: #1e3a8a;
font-size: 30px;
font-weight: 700;
}

.login-subtitle {
text-align: center;
color: #64748b;
margin-bottom: 25px;
}

.login-card {
background-color: #ffffff;
padding: 35px;
border-radius: 18px;
border: 1px solid #e5e7eb;
box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
margin-bottom: 20px;
}

.stButton > button {
border-radius: 8px;
font-weight: 600;
min-height: 42px;
}

div[data-testid="stDataFrame"] {
border-radius: 10px;
overflow: hidden;
}

hr {
border-color: #e5e7eb;
}

.footer {
text-align: center;
color: #64748b;
font-size: 13px;
padding: 25px;
margin-top: 30px;
}
</style>
""",
    unsafe_allow_html=True
)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.markdown(
        """
<div class="login-card">
<div class="login-title">
📋 Attendance Management System
</div>
<div class="login-subtitle">
Secure Administrator Login
</div>
</div>
""",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input(
            "👤 Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter password"
        )

        st.write("")

        login_button = st.button(
            "🔐 Login",
            type="primary",
            use_container_width=True
        )

        if login_button:

            if not username or not password:

                st.warning(
                    "⚠️ Please enter username and password."
                )

            elif login_user(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("✅ Login successful!")

                st.rerun()

            else:

                st.error(
                    "❌ Invalid username or password."
                )

        st.info("Default login: admin / admin123")

    st.markdown(
        """
<div class="footer">
📋 <b>Attendance Management System</b><br>
Student Attendance Tracking Platform<br>
Developed using Python & Streamlit
</div>
""",
        unsafe_allow_html=True
    )

    st.stop()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
<div class="sidebar-title">
    📋 Attendance System
</div>

<div class="sidebar-subtitle">
    Student Attendance Management
</div>
""",
    unsafe_allow_html=True
)

st.sidebar.success(
    f"👤 {st.session_state.username}"
)

st.sidebar.markdown("### Navigation")

menu = st.sidebar.radio(
    "",
    [
        "📊 Dashboard",
        "👨‍🎓 Students",
        "📝 Mark Attendance",
        "📋 Attendance Records",
        "📈 Reports"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    if "username" in st.session_state:
        del st.session_state.username

    st.rerun()

st.sidebar.divider()

st.sidebar.caption(
    "Attendance Management System"
)

st.sidebar.caption(
    "Version 1.0"
)

# ============================================================
# DASHBOARD
# ============================================================

if menu == "📊 Dashboard":

    st.markdown(
        """<div class="welcome-banner"><div class="welcome-title">📊 Attendance Dashboard</div><div class="welcome-text">Welcome to the Attendance Management System.<br>Manage students, attendance and reports from one place.</div></div>""",
        unsafe_allow_html=True
    )

    students = get_students()
    records = get_attendance_records()

    today = str(date.today())

    today_records = [
        record
        for record in records
        if record[4] == today
    ]

    present_today = sum(
        1
        for record in today_records
        if record[5] == "Present"
    )

    absent_today = sum(
        1
        for record in today_records
        if record[5] == "Absent"
    )

    total_today = present_today + absent_today

    attendance_percentage = (
        (present_today / total_today) * 100
        if total_today > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""<div class="dashboard-card"><div class="card-title">👨‍🎓 TOTAL STUDENTS</div><div class="card-value">{len(students)}</div></div>""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""<div class="dashboard-card"><div class="card-title">✅ PRESENT TODAY</div><div class="card-value">{present_today}</div></div>""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""<div class="dashboard-card"><div class="card-title">❌ ABSENT TODAY</div><div class="card-value">{absent_today}</div></div>""",
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""<div class="dashboard-card"><div class="card-title">📊 ATTENDANCE</div><div class="card-value">{attendance_percentage:.1f}%</div></div>""",
            unsafe_allow_html=True
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📅 Today's Summary")

        st.write(
            f"**Date:** {date.today().strftime('%d %B %Y')}"
        )

        st.write(
            f"**Total Students:** {len(students)}"
        )

        st.write(
            f"**Present:** {present_today}"
        )

        st.write(
            f"**Absent:** {absent_today}"
        )

    with col2:

        st.subheader("📌 Quick Actions")

        if st.button(
            "📝 Mark Today's Attendance",
            use_container_width=True
        ):

            st.info(
                "Use 'Mark Attendance' from the sidebar."
            )

        if st.button(
            "👨‍🎓 Manage Students",
            use_container_width=True
        ):

            st.info(
                "Use 'Students' from the sidebar."
            )

    st.divider()

    st.subheader("📋 Today's Attendance")

    if today_records:

        today_data = []

        for record in today_records:

            today_data.append(
                {
                    "Student Name": record[2],
                    "Roll Number": record[3],
                    "Date": record[4],
                    "Status": record[5]
                }
            )

        st.dataframe(
            today_data,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "📌 No attendance has been marked today."
        )

# ============================================================
# STUDENTS
# ============================================================

elif menu == "👨‍🎓 Students":

    st.title("👨‍🎓 Student Management")

    st.caption(
        "Add, search, update and manage student information."
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Student",
            "🔍 Search Students",
            "✏️ Update / Delete"
        ]
    )

    # --------------------------------------------------------
    # ADD STUDENT
    # --------------------------------------------------------

    with tab1:

        st.subheader("➕ Register New Student")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Student Name",
                key="add_name"
            )

            roll_no = st.text_input(
                "Roll Number",
                key="add_roll"
            )

            department = st.text_input(
                "Department",
                key="add_department"
            )

        with col2:

            year = st.selectbox(
                "Year",
                [
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "4th Year"
                ],
                key="add_year"
            )

            section = st.selectbox(
                "Section",
                ["A", "B", "C"],
                key="add_section"
            )

        st.write("")

        if st.button(
            "➕ Add Student",
            type="primary",
            use_container_width=True
        ):

            if name and roll_no and department:

                result = add_student(
                    name.strip(),
                    roll_no.strip(),
                    department.strip(),
                    year,
                    section
                )

                if result:

                    st.success(
                        "✅ Student added successfully!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Roll number already exists."
                    )

            else:

                st.warning(
                    "⚠️ Please fill all required fields."
                )

    # --------------------------------------------------------
    # SEARCH STUDENTS
    # --------------------------------------------------------

    with tab2:

        st.subheader("🔍 Search Students")

        search_text = st.text_input(
            "Search by Name, Roll Number or Department",
            placeholder="Enter search text..."
        )

        if search_text:

            search_results = search_students(
                search_text.strip()
            )

            if search_results:

                search_data = []

                for student in search_results:

                    search_data.append(
                        {
                            "Student ID": student[0],
                            "Name": student[1],
                            "Roll Number": student[2],
                            "Department": student[3],
                            "Year": student[4],
                            "Section": student[5]
                        }
                    )

                st.success(
                    f"Found {len(search_results)} student(s)."
                )

                st.dataframe(
                    search_data,
                    hide_index=True,
                    use_container_width=True
                )

            else:

                st.warning(
                    "❌ No students found."
                )

        else:

            st.info(
                "Enter a search term above."
            )

    # --------------------------------------------------------
    # UPDATE / DELETE
    # --------------------------------------------------------

    with tab3:

        st.subheader(
            "✏️ Update or Delete Student"
        )

        students = get_students()

        if not students:

            st.info(
                "No students available."
            )

        else:

            student_options = {
                f"{student[2]} - {student[1]}": student[0]
                for student in students
            }

            selected_student_name = st.selectbox(
                "Select Student",
                list(student_options.keys())
            )

            selected_student_id = student_options[
                selected_student_name
            ]

            selected_student = next(
                student
                for student in students
                if student[0] == selected_student_id
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                edit_name = st.text_input(
                    "Student Name",
                    value=selected_student[1],
                    key="edit_name"
                )

                edit_roll = st.text_input(
                    "Roll Number",
                    value=selected_student[2],
                    key="edit_roll"
                )

                edit_department = st.text_input(
                    "Department",
                    value=selected_student[3],
                    key="edit_department"
                )

            with col2:

                year_options = [
                    "1st Year",
                    "2nd Year",
                    "3rd Year",
                    "4th Year"
                ]

                section_options = [
                    "A",
                    "B",
                    "C"
                ]

                edit_year = st.selectbox(
                    "Year",
                    year_options,
                    index=(
                        year_options.index(
                            selected_student[4]
                        )
                        if selected_student[4]
                        in year_options
                        else 0
                    ),
                    key="edit_year"
                )

                edit_section = st.selectbox(
                    "Section",
                    section_options,
                    index=(
                        section_options.index(
                            selected_student[5]
                        )
                        if selected_student[5]
                        in section_options
                        else 0
                    ),
                    key="edit_section"
                )

            st.write("")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "💾 Update Student",
                    type="primary",
                    use_container_width=True
                ):

                    if (
                        edit_name
                        and edit_roll
                        and edit_department
                    ):

                        result = update_student(
                            selected_student_id,
                            edit_name.strip(),
                            edit_roll.strip(),
                            edit_department.strip(),
                            edit_year,
                            edit_section
                        )

                        if result:

                            st.success(
                                "✅ Student updated successfully!"
                            )

                            st.rerun()

                        else:

                            st.error(
                                "❌ Roll number already exists."
                            )

                    else:

                        st.warning(
                            "Please fill all fields."
                        )

            with col2:

                if st.button(
                    "🗑️ Delete Student",
                    use_container_width=True
                ):

                    st.session_state[
                        "confirm_delete"
                    ] = True

            if st.session_state.get(
                "confirm_delete",
                False
            ):

                st.warning(
                    f"⚠️ Confirm deletion of "
                    f"{selected_student[1]}?"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Yes, Delete",
                        type="primary",
                        use_container_width=True
                    ):

                        delete_student(
                            selected_student_id
                        )

                        st.session_state[
                            "confirm_delete"
                        ] = False

                        st.success(
                            "✅ Student deleted successfully!"
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "Cancel",
                        use_container_width=True
                    ):

                        st.session_state[
                            "confirm_delete"
                        ] = False

                        st.rerun()

    st.divider()

    st.subheader("📋 All Students")

    students = get_students()

    if students:

        student_data = []

        for student in students:

            student_data.append(
                {
                    "Student ID": student[0],
                    "Name": student[1],
                    "Roll Number": student[2],
                    "Department": student[3],
                    "Year": student[4],
                    "Section": student[5]
                }
            )

        st.dataframe(
            student_data,
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No students registered yet."
        )

# ============================================================
# MARK ATTENDANCE
# ============================================================

elif menu == "📝 Mark Attendance":

    st.title("📝 Mark Attendance")

    st.caption(
        "Record daily attendance for students."
    )

    students = get_students()

    if not students:

        st.warning(
            "⚠️ No students found. Please add students first."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            selected_date = st.date_input(
                "📅 Select Date",
                value=date.today()
            )

        with col2:

            selected_class = st.selectbox(
                "🏫 Select Class",
                [
                    "M.Tech CSE",
                    "M.Tech AI",
                    "B.Tech CSE"
                ]
            )

        st.divider()

        st.info(
            f"📅 Date: {selected_date}   |   "
            f"🏫 Class: {selected_class}"
        )

        existing_records = get_attendance_by_date(
            str(selected_date)
        )

        existing_status = {}

        for record in existing_records:

            student_id = record[0]
            status = record[3]

            if status:
                existing_status[student_id] = status

        attendance_status = {}

        for student in students:

            student_id = student[0]
            student_name = student[1]
            roll_no = student[2]

            default_status = existing_status.get(
                student_id,
                "Present"
            )

            st.markdown(
                f"**{roll_no} — {student_name}**"
            )

            status = st.radio(
                "Attendance",
                ["Present", "Absent"],
                horizontal=True,
                index=(
                    0
                    if default_status == "Present"
                    else 1
                ),
                key=f"attendance_{student_id}",
                label_visibility="collapsed"
            )

            attendance_status[
                student_id
            ] = status

            st.divider()

        if st.button(
            "💾 Save Attendance",
            type="primary",
            use_container_width=True
        ):

            for student_id, status in attendance_status.items():

                save_attendance(
                    student_id,
                    str(selected_date),
                    status
                )

            st.success(
                "✅ Attendance saved successfully!"
            )

# ============================================================
# ATTENDANCE RECORDS
# ============================================================

elif menu == "📋 Attendance Records":

    st.title("📋 Attendance Records")

    st.caption(
        "View all previously recorded attendance."
    )

    records = get_attendance_records()

    if records:

        attendance_data = []

        for record in records:

            attendance_data.append(
                {
                    "ID": record[0],
                    "Student ID": record[1],
                    "Student Name": record[2],
                    "Roll Number": record[3],
                    "Date": record[4],
                    "Status": record[5]
                }
            )

        st.dataframe(
            attendance_data,
            hide_index=True,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "📊 Attendance Statistics"
        )

        total_records = len(records)

        present_records = sum(
            1
            for record in records
            if record[5] == "Present"
        )

        absent_records = sum(
            1
            for record in records
            if record[5] == "Absent"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Records",
                total_records
            )

        with col2:
            st.metric(
                "Present",
                present_records
            )

        with col3:
            st.metric(
                "Absent",
                absent_records
            )

    else:

        st.info(
            "📌 No attendance records found."
        )

# ============================================================
# REPORTS
# ============================================================

elif menu == "📈 Reports":

    st.title("📈 Attendance Reports")

    st.caption(
        "Analyze student attendance performance."
    )

    students = get_students()

    if not students:

        st.info(
            "No students available for reports."
        )

    else:

        report_data = []
        chart_data = {}

        for student in students:

            student_id = student[0]
            student_name = student[1]
            roll_no = student[2]

            total, present, absent = (
                get_student_attendance_summary(
                    student_id
                )
            )

            percentage = (
                (present / total) * 100
                if total > 0
                else 0
            )

            report_data.append(
                {
                    "Student ID": student_id,
                    "Student Name": student_name,
                    "Roll Number": roll_no,
                    "Total Classes": total,
                    "Present": present,
                    "Absent": absent,
                    "Attendance %": f"{percentage:.1f}%"
                }
            )

            chart_data[
                roll_no
            ] = percentage

        st.subheader(
            "📊 Overall Attendance Report"
        )

        st.dataframe(
            report_data,
            hide_index=True,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "📊 Attendance Percentage"
        )

        if any(
            value > 0
            for value in chart_data.values()
        ):

            st.bar_chart(
                chart_data,
                y_label="Attendance Percentage",
                x_label="Roll Number"
            )

        else:

            st.info(
                "No attendance data available for the chart."
            )

        st.divider()

        st.subheader(
            "🔎 Individual Student Report"
        )

        student_options = {
            f"{student[2]} - {student[1]}": student[0]
            for student in students
        }

        selected_student_name = st.selectbox(
            "Select Student",
            list(student_options.keys())
        )

        selected_student_id = student_options[
            selected_student_name
        ]

        selected_student = next(
            student
            for student in students
            if student[0] == selected_student_id
        )

        total, present, absent = (
            get_student_attendance_summary(
                selected_student_id
            )
        )

        percentage = (
            (present / total) * 100
            if total > 0
            else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Classes",
                total
            )

        with col2:
            st.metric(
                "Present",
                present
            )

        with col3:
            st.metric(
                "Absent",
                absent
            )

        with col4:
            st.metric(
                "Attendance %",
                f"{percentage:.1f}%"
            )

        if total > 0:

            if percentage < 75:

                st.warning(
                    "⚠️ Attendance is below 75%."
                )

            else:

                st.success(
                    "✅ Attendance is 75% or above."
                )

        st.divider()

        st.subheader(
            f"📅 Attendance History - "
            f"{selected_student[1]}"
        )

        history = get_student_attendance(
            selected_student_id
        )

        if history:

            history_data = []

            for record in history:

                history_data.append(
                    {
                        "Date": record[0],
                        "Status": record[1]
                    }
                )

            st.dataframe(
                history_data,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "No attendance records available for this student."
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
📋 <b>Attendance Management System</b><br>
Student Attendance Tracking Platform<br>
Developed using Python & Streamlit
</div>
""",
    unsafe_allow_html=True
)