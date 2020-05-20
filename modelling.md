## Covid modelling

###Objective
Get a forecast on the number of infected and hospitalized

###Data
USE John Hopkins repository

###Modelling
For now I we make the assumption that the most reliable figure to calibrate the model on is the number of deceased.

Per country of focus create base file with following parameters:
* relative fraction of infected people hospitalized (hosfrac): default set at 0.05. To do: look for better estimates 
* hospitalization case fatality rate (dfrac): 0.22 similar to China taken. To do: look for better estimates <br>
Note: model seems to focus of people who are hospitalized and die through hospitalization case fatality rate
and fraction of ICU patients dying. This does not seem to incoporate Covid19 deaths without going to the hospital.
To do: find how the number of Covid19 deaths are administered. And if this is different than the model, adapt the 
model accordingly. Also the hospitalization case fatality rate is a fixed number for which a good estimate is needed.
* fraction of hospitalized patients in need for ICU (ICufrac): 0.0. Initially set at 0 so no patients are going to the ICU.
For now this means that from all covid patients arriving the hospital the hospitalization case fatality rate will die and 
the rest will recover. 

* "worldfile": true ; use data from USE John Hopkins repository
* startdate of SEIR model: this is the 'startdate'  - 'time_delay' <br>
Note: the difference of using a time delay of 0 with a start date t or using a time delay of 1 and a startdate of t+1
is,  that actual data of day t is not used, see file imput_data.txt. If I understand correctly this data is used to assess 
the performance of the model. In the cases you often see a delay of 8 days or more. This is presumably done to ignore 
the first 'noisy' days in fitting the model. To do: check if this is correct.
The startdate in the modelling in the Netherlands is March 1st with a time delay of 8 days. Meaning the modelling started
at February 22nd. The first death was the 6th of March and the number has been increasing from that day onward, 
so this was not an incidental death. The 10th dead was registered on the 13th of March.
As a 'quick and dirty'starter rule of thumb choose the startdate 19-21 days before the 10th death and possibly use a delay.

* initial seed of exposed persons 1/N, 1 out of N. If N is low then there is high exposure. Difficult to set a value so
we start of with a large range min:50000,max 500000. These numbers can be adjusted depending whether at the startdate 
of the model a larger of smaller part of the country was affected. For example if there are mutiple outbreaks already. 
* R0, for now data is used similar to other cases, uniform between min: 3.3 and max 3.7. To do: see if there is 
data/research that approves or disproves this value for the specific countries.
* alpha and dayalpha: first approach is to fit alpha per week from a broad ranch. So a dayalpha is set at day 0,7,14, etc.
If the model statrs early in the outbreak without distancing measures in place the first two weeks are taken together. 
The last period begins about 2-3 weeks before the last date there is data of, so there is data to calibrate on 
(death occur at a delay). The ranges can be somehow limited dependent on the social distancing measure in place at that moment.

Information per country can be found online or from country offices. Wikipedia seems to have a lot of information on reported cases and
taken measures. For example for [Africa](https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Africa) and for [Kenya](https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Kenya).

