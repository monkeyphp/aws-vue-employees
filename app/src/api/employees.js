/**
 * @file employees.js
 */
import axios from 'axios';

/* eslint-disable */

export default {
    /**
     * Return a list of Employees
     *
     * @param parent_group_id
     * @returns {Promise<any>}
     */
    employees_get(parent_group_id = null) {
        let params = {};

        if (parent_group_id) {
            params['parent_group_id'] = parent_group_id
        }

        console.log(parent_group_id);
        console.log(params);

        return new Promise((resolve, reject) => {
            axios.get(`/employees`, params)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Return the Employees that have been added to the Group identified by the
     * supplied group_id
     *
     * @param group_id
     * @returns {Promise<any>}
     */
    group_employees_get (group_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/groups/${group_id}/employees`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Post an employee object to the api
     *
     * @param employee
     * @returns {Promise<any>}
     */
    employees_post(employee) {
        return new Promise((resolve, reject) => {
            axios.post(`/employees`, employee)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Return the employee identified by the supplied employee_uuid
     *
     * @param employee_uuid
     * @returns {Promise<any>}
     */
    employee_get(employee_uuid) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_uuid}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
            });
    },
    /**
     * Put an employee object
     *
     * @param employee
     * @returns {Promise<any>}
     */
    employee_put (employee) {
        const employee_id = employee.employee_id;
        return new Promise((resolve, reject) => {
            axios.put(`/employees/${employee_id}`, employee)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Delete the Employee identified by the supplied employee_uuid
     *
     * @param employee_uuid
     * @returns {Promise<any>}
     */
    employee_delete (employee_uuid) {
        return new Promise((resolve, reject) => {
            axios.delete(`/employees/${employee_uuid}`)
                .then(() => {
                    resolve();
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },

    /**
     * Return a list of Timesheets for the specified Employee
     *
     * @param employee_id
     * @returns {Promise<any>}
     */
    employee_timesheets_get(employee_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_id}/timesheets`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Return the Timesheet for the specified Employee on the specified date
     *
     * @param employee_id
     * @param date
     * @returns {Promise<any>}
     */
    employee_timesheet_get(employee_id, date) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_id}/timesheets/${date}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },


    /**
     * Return a list of Entries for the specified Employee and date
     *
     * @param employee_id
     * @param date
     * @returns {Promise<any>}
     */
    employee_timesheet_entries_get(employee_id, date) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_id}/timesheets/${date}/entries`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Post a new Entry
     *
     * @param employee_id
     * @param entry
     * @returns {Promise<any>}
     */
    employee_timesheet_entries_post(employee_id, entry) {
        return new Promise((resolve, reject) => {
            const date = entry['date'];
            axios.post(`/employees/${employee_id}/timesheets/${date}/entries`, entry)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Return the Entry identigied by the supplied employee_id, date and time
     *
     * @param employee_id
     * @param date
     * @param time
     * @returns {Promise<any>}
     */
    employee_timesheet_entry_get(employee_id, date, time) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_id}/timesheets/${date}/entries/${time}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                })
        });
    },
    /**
     * Delete the Entry identified by the supplied employee_id, date, time
     *
     * @param employee_id
     * @param date
     * @param time
     * @returns {Promise<any>}
     */
    employee_timesheet_entry_delete(employee_id, date, time) {
        return new Promise((resolve, reject) => {
            axios.delete(`/employees/${employee_id}/timesheets/${date}/entries/${time}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                })
        });
    },
    /**
     * Return a list of Contracts that belong to the specified Employee
     *
     * @param employee_id
     * @returns {Promise<any>}
     */
    employee_contracts_get(employee_id) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_id}/contracts`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Post a Contract for the specified Employee
     *
     * @param employee_id
     * @param employee_contract
     * @returns {Promise<any>}
     */
    employee_contracts_post(employee_id, employee_contract) {
        return new Promise((resolve, reject) => {
            axios.post(`/employees/${employee_id}/contracts`, employee_contract)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Return the Contract identified by the supplied date
     *
     * @param employee_id
     * @param start_date
     * @returns {Promise<any>}
     */
    employee_contract_get(employee_id, start_date) {
        return new Promise((resolve, reject) => {
            axios.get(`/employees/${employee_id}/contracts/${start_date}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Delete the Contract identified by the supplied start date
     *
     * @param employee_id
     * @param start_date
     * @returns {Promise<any>}
     */
    employee_contract_delete(employee_id, start_date) {
        return new Promise((resolve, reject) => {
            axios.delete(`/employees/${employee_id}/contracts/${start_date}`)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    },
    /**
     * Update the specified Contract
     *
     * @param employee_id
     * @param start_date
     * @param contract
     * @returns {Promise<any>}
     */
    employee_contract_put(employee_id, start_date, contract) {
        return new Promise((resolve, reject) => {
            axios.put(`/employees/${employee_id}/contracts/${start_date}`, contract)
                .then((response) => {
                    const data = response.data;
                    resolve(data);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    }
};
