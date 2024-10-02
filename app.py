from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Route สำหรับฝั่งผู้เช่า
@app.route('/tenant')
def tenant_home():
    return render_template('tenant_home.html')

@app.route('/tenant/costs')
def tenant_view_costs():
    # ดึงข้อมูลค่าใช้จ่ายห้องพักของผู้เช่าจากฐานข้อมูล
    costs = {
        'rent': 5000,
        'water': 300,
        'electricity': 500,
        'total': 5800
    }
    return render_template('tenant_view_costs.html', costs=costs)

@app.route('/tenant/report', methods=['GET', 'POST'])
def tenant_report_issue():
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        issue_description = request.form['issue_description']
        # บันทึกการแจ้งชำรุดในฐานข้อมูล
        # ...
        return redirect(url_for('tenant_home'))
    return render_template('tenant_report_issue.html')

# Route สำหรับฝั่งเจ้าของหอพัก
@app.route('/owner')
def owner_home():
    return render_template('owner_home.html')

# Route สำหรับจัดการห้องพัก (เหมือนเดิม)
@app.route('/owner/rooms')
def owner_manage_rooms():
    # สร้างห้องตัวอย่าง 30 ห้อง
    rooms = []
    for i in range(1, 31):
        if i % 3 == 0:
            status = 'Occupied'  # มีผู้พักอยู่
            tenant = {
                'name': 'Tenant ' + str(i),
                'contract_duration': '12 months',
                'contact_info': 'tenant' + str(i) + '@example.com'
            }
        elif i % 2 == 0:
            status = 'Under Maintenance'  # กำลังปรับปรุง
            tenant = None
        else:
            status = 'Available'  # ว่าง
            tenant = None

        rooms.append({
            'room_no': f'{i:03}',
            'status': status,
            'tenant': tenant
        })

    return render_template('owner_manage_rooms.html', rooms=rooms)

# Route สำหรับดูรายละเอียดห้อง
@app.route('/owner/room/<room_no>', methods=['GET', 'POST'])
def owner_room_detail(room_no):
    # จำลองข้อมูลห้องที่ต้องการดูรายละเอียด
    room = {
        'room_no': room_no,
        'status': 'Occupied' if int(room_no) % 3 == 0 else ('Under Maintenance' if int(room_no) % 2 == 0 else 'Available'),
        'tenant': {
            'name': 'Tenant ' + room_no,
            'contract_duration': '12 months',
            'contact_info': 'tenant' + room_no + '@example.com'
        } if int(room_no) % 3 == 0 else None
    }

    if request.method == 'POST':
        if 'add_tenant' in request.form:
            # เพิ่มผู้เช่าใหม่และเปลี่ยนสถานะเป็น 'Occupied'
            room['tenant'] = {
                'name': request.form['tenant_name'],
                'contract_duration': request.form['contract_duration'],
                'contact_info': request.form['contact_info']
            }
            room['status'] = 'Occupied'
        elif 'set_available' in request.form:
            # เปลี่ยนสถานะเป็น 'Available'
            room['tenant'] = None
            room['status'] = 'Available'

    return render_template('owner_room_detail.html', room=room)

@app.route('/owner/reports')
def owner_view_reports():
    # ดึงข้อมูลการแจ้งซ่อมจากผู้เช่าจากฐานข้อมูล
    reports = [
        {'room_no': '101', 'issue': 'ไฟเสีย', 'status': 'Pending'},
        {'room_no': '102', 'issue': 'แอร์ไม่เย็น', 'status': 'In Progress'}
    ]
    return render_template('owner_view_reports.html', reports=reports)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
