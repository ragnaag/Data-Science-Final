# Data-Science-Final


This data was gathered for Tech Money Busters' final project for CS1951a (Spr2020).
Tech Money Busters is Jacob DiSpirito (jdispiri), Lauren Yang (kyang28),
Ragna Agerup (ragerup), and Shira Abramovich (sabramo1).

-------------------------------------------------------------------------------

Our data is in tbm_data.db

Sample of data:
https://docs.google.com/spreadsheets/d/18hOUO8Pj5KuFky8RJOJ9Z0tHWb-3exsNHR3-6glSC-0/edit?usp=sharing


I. Where the data is from

We have scraped our data from pages on opensecrets.org, a site which aggregates
campaign finance and lobbying data from various sources (including the Federal
Election Commission and lobbying reports). OpenSecrets is part of the Center
for Responsive Politics, which researches and tracks money in US politics
with the goal of “produc[ing] and disseminat[ing] peerless data and analysis
on money in politics to inform and engage Americans, champion transparency,
and expose disproportionate or undue influence on public policy.”

II. Format of the data

	The data is stored in a SQL database and is divided into two tables:
	pac_donations and candidate_donations. The formats of each are as follows:

	pac_donations (26 columns, 152 rows):
		i. pacid: PAC IDs are a list of unique identifiers of each PAC, varchar(255),
		listed on the open secrets website, starting with letter C and followed by 8 digits.

		ii: pacname: These are the names of the PAC, varchar(255), this is the primary
		key of this table documenting unique identifiers of each PAC donations.

		iii-xxvi: for each election cycle(2010, 2012, 2014, 2016, 2018, and 2020), we
		have four recurring columns specified below:
		   Affiliate: varchar(255), the affiliate indicates an organization that
		   		the PACs are associated with. If there is no affiliate, it is specified
				as null.
		   year-Total: integer, Total documents the total amount of donations from
		   		a PAC during a specific year.
		   year-Dems: integer, Dems documents the total amount of donations from a
			   	PAC to democratic candidates during a specific year.
		   year-Repub: Repub documents the total amount of donations from a PAC to
			   	republican candidates during a specific year.

	candidate_donations (9 columns, 13473 rows):
		i. donation_id: an auto-generated auto-incremented key, an integer,
			that serves as the unique primary key for each donation.

		ii. company_id: the company id associated with the company, a varchar(255),
			taken from the URL. Because multiple company names can correspond to the
			same ID in the case of a name change or buyout, this is not a unique foreign key.

		iii. company_name: the company name, a /Users/ragnaag/Downloads/data-spec.txtvarchar(255), 
			a foreign key that references the pacname column in the pac_donations table and refers
			to the name of the PAC which is donating.

		iv. candidate_name: the name of the candidate, a varchar(255), with the format
			“Lastname, Firstname”

		v. race: the name of the race or chamber for which the candidate is running,
			a varchar(255). The options are Presidential, House, and Senate.

		vi. party: the party to which a candidate belongs, a varchar(255). The options
			are D (for Democrat), R (Republican), I (Independent), and U (undeclared).

		vii. state: the abbreviation for the state or district in which a candidate is
			running, a varchar(255). This field is Null when the candidate is running
			for president.

		viii. amount: the dollar amount of the donation, an integer.

 		ix. year: the year or cycle of the election. The options are 2010, 2012,
	   		2014, 2016, 2018, and 2020.
