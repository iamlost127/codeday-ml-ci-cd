# Continuous Integration and Continuous Delivery for Machine Learning

**What is CI/CD**

***Continuous Integration*** is a software development practice where members of a team integrate their work frequently, 
usually each person integrates at least daily - leading to multiple integrations per day. 
Each integration is verified by an automated build (including test) to detect integration errors 
as quickly as possible. This approach leads to significantly reduced 
integration problems and allows a team to develop cohesive software more rapidly

***Continuous Delivery*** is the ability to get changes of all types — including new features, configuration changes, bug fixes, and experiments — into production, or into the hands of users, safely and quickly in a sustainable way".
-- Jez Humble and Dave Farley

The key test is that a *business sponsor could request that the current development version of the 
software can be deployed into production at a moment's notice* - and nobody would bat an eyelid, let alone panic.

**How are Machine Learning Applications different from usual Software Applications**
The process for developing, deploying, and continuously improving them is much more complex compared 
traditional software, such as a web service or a mobile application. Since ML Applications are subject to change in 
three axis: the code itself, the model, and the data. Their behaviour is often complex 
and hard to predict, and they are harder to test, harder to explain, and harder to improve
