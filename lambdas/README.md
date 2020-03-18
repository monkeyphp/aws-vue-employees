# Timesheets

## Activities

Activities can be assigned to Entries to record what the Employee was doing.

- `activity_id` is the internal identifier for the Activity.
- `name` is the application identifier for the Activity.
- `code` is the Customer supplied identifier for the Activity.
- `description` is the human friendly description of the Activity.
- `worked` is a boolean that indicates that the entry is considered as being a paid activity or not.
- `created` is the timestamp when the Activity was first created.

```python
activity = {
    'activity_id': 'working',
    'name': 'Working',
    'code': 'W',
    'description': 'A brief description of the Activity',
    'worked': True,
    'created': '2020-01-01 13:45:34',
}
```

## Employees

- `employee_id` is the client supplied Employee Id.
- `name` is the Employees full name.
- `parent_group_id` is the id of the Group the Employee belongs to.
- `created` is the timestamp when the Employee was first created. 

```python
employee = {
    'employee_id': '1000',
    'name': 'Albert Andrews',
    'parent_group_id': 'all',
    'created': '2020-01-01 13:45:34',
}
```

### Contracts

Contracts are a sub resource of Employees.

- `start_date` (primary key) The date that the Contract commences.
- `weekly_hours` (Optional)
- `hourly_rate` (Optional)

```python
contract = {
    'employee_id': '1000',
    'start_date': '2019-01-01',
    'weekly_hours': '40',
    'hourly_rate': '856',
    'created': '2020-01-08 15:39:54'
}
```

### Timesheets

```python
timesheet = {
    'employee_id': '1000',
    'date': '2020-01-13',
}
```

## Entries

```python
entries = {
    'employee_id': '1000',
    'date': '2020-01-13',
    'start_time': '09:00',
    'finish_time': '17:00',
    'activity': 'working',
    'created': '2020-01-13 10:25:17',
}
```

## Groups

Groups are collections of Employees and other Groups. 
A Group could represent an entire organisation, a region, a store or a department.
A hard coded `ALL` group is included as part of the application.

- `group_id` is the id of the Group.
- `name` is the name of the Group.
- `description` is the description of the Group.
- `created` is the timestamp the Group was first created.
- `parent_group_id` is the group id of the parent Group.

```python
groups = [
    {
        'group_id': "all",
        'name': "All",
        'description': 'Default ALL group',
        'created': "2020-01-08 15:39:49.565289+00:00",
    },
    {
        'group_id': "stores",
        'name': "Stores",
        'description': 'Stores Group',
        'parent_group_id': 'all',
        'created': "2020-01-08 15:39:49.565289+00:00",
    }
]
```



















- get_employees()
- save_employee(employee)
- get_employee(employee_uuid)
- delete_employee(employee)
- get_employee_timesheets(employee_uuid)
- get_employee_timesheet(employee_uuid, date)
- save_employee_timesheet(timesheet)

- get_employee_timesheet_entries(employee_uuid, date=None)
- get_employee_timesheet_entry(employee_uuid, date, time)
- save_employee_timesheet_entry(entry)
- delete_employee_timesheet_entry(entry)
- get_employee_contracts(employee_uuid)
- get_employee_contract(employee_uuid, date)
- save_employee_contract(contract)
delete_employee_contract(contract)

get_activities()
save_activity(activity)
get_activity(activity_uuid)
delete_activity(activity_uuid)

# /employees [GET]
# /employees [POST]

# /employees/{employee_uuid} [GET]
# /employees/{employee_uuid} [PUT]
# /employees/{employee_uuid} [DELETE]

# /employees/{employee_uuid}/timesheets [GET]
# /employees/{employee_uuid}/timesheets/{date} [GET]

# /employees/{employee_uuid}/timesheets/{date}/entries [GET]
# /employees/{employee_uuid}/timesheets/{date}/entries [POST]

# /employees/{employee_uuid}/timesheets/{date}/entries/{time} [GET]
# /employees/{employee_uuid}/timesheets/{date}/entries/{time} [DELETE]

# /employees/{employee_uuid}/contracts [GET]
# /employees/{employee_uuid}/contracts [POST]
# /employees/{employee_uuid}/contracts/{date} [GET]
# /employees/{employee_uuid}/contracts/{date} [DELETE]

# /activities [GET]
# /activities [POST]
# /activities/{activity_uuid} [GET]
# /activities/{activity_uuid} [DELETE]


----

# /employee-groups [GET]
# /employee-groups [POST]
# /employee-groups/{employee_group_uuid} [GET]
# /employee-groups/{employee_group_uuid} [DELETE]
# /employee-groups/{employee_group_uuid}/employee-groups [GET]
# /employee-groups/{employee_group_uuid}/employee-groups [POST]
# /employee-groups/{employee_group_uuid}/employees [GET]
# /employee-groups/{employee_group_uuid}/employees [POST]

# /employee-groups/{employee_group_uuid}/employee-groups/{sub_employee_group_uuid} [GET]
# /employee-groups/{employee_group_uuid}/employee-groups/{sub_employee_group_uuid} [DELETE]
# /employee-groups/{employee_group_uuid}/employees/{employee_uuid} [GET]
# /employee-groups/{employee_group_uuid}/employees/{employee_uuid} [DELETE]



datetime.datetime.now().replace(microsecond=0,second=0).isoformat()

datetime.datetime.now().replace(microsecond=0).isoformat()
datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()
https://stackoverflow.com/questions/2150739/iso-time-iso-8601-in-python

http://www.cpearson.com/Excel/overtime.htm

aws dynamodb batch-write-item --request-items file://request-items-map.json