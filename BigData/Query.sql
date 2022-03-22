/*
# day-by-day active chargers and number of reports
# save to dayactive.txt
drop table if exists tt1;

create table tt1
select date(ts) as dd, count(distinct station, charger) as alive
from OpStatus
group by dd;

drop table if exists tt2;

create table tt2
select date(ts) as dd, count(*) as numreport
from OpStatus
group by dd;

select tt1.dd, tt1.alive, tt2.numreport
from tt1, tt2
where tt1.dd = tt2.dd;
*/


/*
# All-region Daily utilization
# save to dayutil.txt
drop table if exists tt1;
create table tt1
select date(ts) as dd, count(*) as cnt
from OpStatus
group by dd;

drop table if exists tt2;
create table tt2
select date(ts) as dd, count(*) as cnt
from OpStatus
where onoff=2
group by dd;

select tt1.dd, tt2.cnt/tt1.cnt 
from tt1 left join tt2 
on tt1.dd=tt2.dd
order by dd;
*/

/*
# all-time charger-by-charger utilization 
# save to chargerutil.txt
drop table if exists tt1;
create table tt1
select station, charger, count(*) as cnt
from OpStatus
group by station, charger;

drop table if exists tt2;
create table tt2
select station, charger, count(*) as cnt
from OpStatus
where onoff=2
group by station, charger;

select tt1.station, tt1.charger, tt2.cnt/tt1.cnt as util
from tt1 left join tt2 
on tt1.station=tt2.station and tt1.charger=tt2.charger
order by util desc;
*/

/*
# All-time all-region hour-of-day utilization
# save to sch.txt
drop table if exists tt1;
create table tt1
select station, charger, hour(ts) as hs, count(*) as cnt
from OpStatus
group by station, charger, hs;

drop table if exists tt2;
create table tt2
select station, charger, hour(ts) as hs, count(*) as cnt
from OpStatus
where onoff=2
group by station, charger, hs;

select tt1.station, tt1.charger, tt1.hs, tt2.cnt/tt1.cnt as util
from tt1 left join tt2 
on tt1.station=tt2.station and tt1.charger=tt2.charger and tt1.hs=tt2.hs
order by util desc;
*/


/*
# All-time all-region day-of-week utilization
# save to wday.txt
drop table if exists tt1;
create table tt1
select dayofweek(ts) as wd, count(*) as cnt
from OpStatus
group by wd;

drop table if exists tt2;
create table tt2
select dayofweek(ts) as wd, count(*) as cnt
from OpStatus
where onoff=2
group by wd;

select tt1.wd, tt2.cnt/tt1.cnt as util
from tt1 left join tt2 
on tt1.wd=tt2.wd 
order by tt1.wd;
*/

/*
# All-time all-region per-type utilization
# just run and cut and paste the result (not so much)
drop table if exists ttt;

create table ttt
select chargers.interface as infc, OpStatus.onoff as onoff
from chargers, OpStatus
where chargers.station=OpStatus.station and chargers.charger=OpStatus.charger;

drop table if exists tt1;
create table tt1
select infc, count(*) as cnt
from ttt
group by infc;

drop table if exists tt2;
create table tt2
select infc, count(*) as cnt
from ttt
where onoff=2
group by infc;

select tt1.infc, tt2.cnt/tt1.cnt as util
from tt1 left join tt2 
on tt1.infc=tt2.infc ;

drop table ttt;
*/

/*
# Location included results
# save to loc.txt
drop table if exists tt1;
create table tt1
select station, charger, count(*) as cnt
from OpStatus
group by station, charger;

drop table if exists tt2;
create table tt2
select station, charger, count(*) as cnt
from OpStatus
where onoff=2
group by station, charger;

drop table if exists tt3;
create table tt3
select tt1.station, tt1.charger, tt2.cnt/tt1.cnt as util
from tt1, tt2
where tt1.station=tt2.station and tt1.charger=tt2.charger;

select chargers.lon, chargers.lat, chargers.interface, tt3.station,tt3.charger, tt3.util
from tt3, chargers
where tt3.station=chargers.station and tt3.charger=chargers.charger
order by util desc;
*/
