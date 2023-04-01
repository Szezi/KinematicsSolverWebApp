<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Szezi/KinematicsSolverWebApp">
    <img src="static\screen\dashboard.png" alt="Dashboard">
  </a>
<h3 align="center">KinematicsSolverWebApp</h3>
  <p align="center">
KinematicsSolverWebApp is a web application that allows users to create multi-users robotic projects to calculate Forward and Inverse Kinematics. 
Application allows user to fill information about themselves in profile page and see stats on dashboard. <br />
    <a href="https://github.com/Szezi/KinematicsSolverWebApp"><strong>Explore the docs »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
      <ul>
        <li><a href="#technologies">Technologies</a></li>
      </ul>
    </li>
    <li><a href="#about-yhe-project">About the project</a></li> 
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- GETTING STARTED -->
## Getting Started

To run this project, clone repo, run docker desktop and run server.

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/Szezi/KinematicsSolverWebApp
   ```
2. Run Docker Desktop
   
3. Build docker image
    ```sh
   $ docker-compose build
   ```
4. Migrate
    ```sh
   $ docker-compose run web python manage.py migrate
   ```
5. Create superuser
    ```sh
   $ docker-compose run web python manage.py createsuperuser
   ```
6. Run server
    ```sh
   $ docker-compose up 
   ```


### Technologies

* [Python](https://www.python.org/downloads/release/python-390/)
* [Django](https://www.djangoproject.com)
* [PostgreSQL](https://www.postgresql.org)
* [Docker](https://www.docker.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ABOUT THE PROJECT -->
## About The Project
KinematicsSolverWebApp is a web application that allows users to create multi-users robotic projects. Application allows user to fill information about themselves in profile page and see stats on dashboard. <br />
To see different pages of application user need to be logged in. If unauthorised user try to view other pages will be automatically redirect to Home page.

Frontend design is based on :https://www.creative-tim.com/product/soft-ui-dashboard

### Home page

<div align="center">
<img src="static\screen\home.png" alt="home">
</div>

Application welcome user with home page. It allows user to log in or create new account.
If user is already logged in it automatically redirect user to dashboard page. Moreover, if user is logged in it is forbidden to create new account.


### Profile

<div align="center">
<img src="static\screen\user.png" alt="user">
</div>

User during registration add avatar, description and basic information about user. AbstractUser was used.

### Dashboard

<div align="center">
<img src="static\screen\dashboard.png" alt="dashboard">
</div>

Dashboard page allows user to keep track with basic information about users projects. 
On top there are stats with numer of projects, numer of calculated Forward and Inverse Kinematics and current date.
On dashboard page user also can create new robotic project and add new robot, keep track on projects is administrator of and see last created robot parameters.

### Robotic Project
<div align="center">
<img src="static\screen\project_create.png" alt="project">
</div>

User can create new project. During creation user can select admins and members of the project.

<div align="center">
<img src="static\screen\project.png" alt="project">
</div>

Project page contains buttons to edit and delete project on the project header bar.
Only administrator can edit or delete project. Another members ae redirected to dashboard page.

User can also add robotic arms to the project and list them in the table.

### Robotic Arm
<div align="center">
<img src="static\screen\robot_create.png" alt="robot">
</div>

User can create new robotic arm for calculations. During creation user fill information about robot, add notes and select project.

<div align="center">
<img src="static\screen\robot.png" alt="robot">
</div>

Robot page contains buttons to edit and delete robot on the robot header bar.
Only member of the project can edit or delete robot. Another users are redirected to dashboard page.

On this page user can create/edit forward and inverse kinematics with parameters filled during robot creation.

### Forward Kinematics
<div align="center">
<img src="static\screen\fk_info.png" alt="robot">
</div>

Page use UpdateView and display information about calculation. User can calculate forward kinematics giving thetas values.

### Inverse Kinematics

<div align="center">
<img src="static\screen\ik_info.png" alt="robot">
</div>

Page use UpdateView and display information about calculation. User can calculate inverse kinematics giving xyz values.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GPL-3.0 license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/Szezi/KinematicsSolverWebApp](https://github.com/Szezi/KinematicsSolverWebApp)

<p align="right">(<a href="#top">back to top</a>)</p>