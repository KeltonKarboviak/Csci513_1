# CSci513_1

This is my submission for the Advanced Database course (CSCI 513) at the University of North Dakota. The project requirements can be found at <http://wenchen.cs.und.edu/course/513/2/1.html>.

## How To Use

1. Clone the repository.

```bash
git clone https://github.com/KeltonKarboviak/CSci513_1.git
```

2. Create a .env file for the Oracle DB credentials and the admin password. An example of the environment keys can be found in .env.example.

```bash
cp .env.example .env
cp java.env.example java.env
```

3. Download the [Open Iconic](https://useiconic.com/open) icon set into the project root.

```bash
wget -O open-iconic.zip http://github.com/iconic/open-iconic/archive/master.zip
unzip open-iconic.zip
rm open-iconic.zip
```

4. Download a local version of jQuery

```bash
mkdir js/vendor
wget -O js/vendor/jquery-3.2.1.min.js https://code.jquery.com/jquery-3.2.1.min.js
```

5. Create python virtual environment & install dependencies. This is assuming you already have `pip` installed.

```bash
pip install virtualenv

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

> Note: the virtualenv can be deactivated simply by running the below

``` bash
deactivate
```

6. Compile java files.

```bash
javac cgi-bin/*.java
```

7. Update file permissions

```bash
chmod -R 755 cgi-bin
```
