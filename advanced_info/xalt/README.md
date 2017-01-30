## XALT: Getting details for a given executable

* Go to [http://tpc14.cscs.ch/xalt-portal.git/xalt_dashboard_cscs.html](http://tpc14.cscs.ch/xalt-portal.git/xalt_dashboard_cscs.html)
and choose dates.

<img src="img/xalt_cscs_top10exe_startpage.png" alt="xalt_cscs_top10exe_startpage" >

---
### Top 10 Executables (Bubble chart and data table)

* Clicking on the submit button will show the Top 10 Executables:

<img src="img/xalt_cscs_top10exe_bubblechart.png" alt="xalt_cscs_top10exe_bubblechart" height="500px" >

---
* Same data inside a table: 

<img src="img/xalt_cscs_top10exe_table.png" alt="xalt_cscs_top10exe_table" >

---
### Finding users running a given executable 

* To find who used a given executable (`alsuqcli` for instance), go to [http://tpc14.cscs.ch/xalt-portal.git/xalt_identify.html](http://tpc14.cscs.ch/xalt-portal.git/xalt_identify.html) and enter the executable name:

<img src="img/xalt_cscs_top10exe_finding_username.png" alt="xalt_cscs_top10exe_finding_username" >

---
## Getting details for a given User ID (CSCS DB)

* Go to [http://tpc14.cscs.ch/xalt-portal.git/xaltindex.html](http://tpc14.cscs.ch/xalt-portal.git/xaltindex.html)
and enter a `UserID` (syshost and dates are ignored). The result for user `klye` is:

<img src="img/xalt_cscs_top10exe_username_details.png" alt="xalt_cscs_top10exe_username_details" >

---
### Multiple Groups
* It also works for user having more than 1 gid:

<img src="img/xalt_cscs_listgid_listexes.png" alt="xalt_cscs_listgid_listexes" >

---
### Project details
* Selecting one of the row in the first table will display more details for the
selected project id
    * for instance for project `s715`:
<img src="img/xalt_cscs_pi+usage_gids715.png" alt="gids715" height="200px" >

    * and for project `u1`:
<img src="img/xalt_cscs_pi+usage_gidu1.png" alt="gidu1" height="300px" >

---
### Troubleshooting
* If a user did not use its allocation, then a table may be empty:
<img src="img/xalt_cscs_pi+usage_gids663.png" alt="gids663" height="200px" >

    * as confirmed by `sbucheck`:
<img src="img/xalt_cscs_pi+usage_gids663_zero.png" alt="gids663_zero" >

