# Project Name

Swiss style tournament pairings and results.

## Installation

Install the virtualbox platform package for your operating system.

Install the version of vagrant for your operating system. Download it from vagrantup.com.

Using the terminal, navigate to the vagrant directory (the outermost directory of this submission).

Run the command `vagrant up` to download and install the linux operating system.
When that is finished, run the command `vagrant ssh` to log into the newly installed VM.


## Usage

While in the VM, navigate to `/vagrant/tournament`.

Open PostgreSQL by running the command `psql` and then run the command `\i tournament.sql` to create the database and tables.

Exit psql by running the command `\q`.

Run the command `python tournament_test.py` to run the unit tests on my module.
