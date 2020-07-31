## Continuous Integration and Continuous Delivery for Machine Learning Applications

_**Continuous Integration**_ is a software development practice where members of a team integrate their work frequently, usually, each person integrates at least daily - leading to multiple integrations per day. Each integration is verified by an automated build (including test) to detect integration errors as quickly as possible. This approach leads to significantly reduced integration problems and allows a team to develop cohesive software more rapidly

_**Continuous Delivery**_ is the ability to get changes of all types — including new features, configuration changes, bug fixes, and experiments — into production, or into the hands of users, safely and quickly in a sustainable way". -- Jez Humble and Dave Farley

The key test is that a _business sponsor could request that the current development version of the software can be deployed into production at a moment's notice_ - and nobody would bat an eyelid, let alone panic.

## How are ML applications different from traditional software applications?

#### Traditional Software Application Workflow
![](https://github.com/iamlost127/codeday-ml-ci-cd/blob/master/images/classic_pipeline.PNG)

The process for developing, deploying, and continuously improving ML applications is much 
more complex compared to traditional software, such as a web service or a mobile application. 
Since ML Applications are subject to change in three axes: the code itself, the model, 
and the data. Their behavior is often complex and hard to predict, and they are harder to test, 
harder to explain, and harder to improve.
Besides the code, changes to ML models and the data used to train them are another type of 
change that needs to be managed and baked into the software delivery process
![](https://github.com/vivekkr12/codeday-ml-ci-cd/blob/master/images/ML%20applications.PNG)

#### Components in ML Applications (Elements for ML systems. Adapted from Hidden Technical Debt in Machine Learning Systems)
![](https://github.com/iamlost127/codeday-ml-ci-cd/blob/master/images/ComponetsinML.PNG)


#### Challenges in ML Applications in production:

1)Team Skills

2) Development

3)Testing

4) Deployment

5)Production

### Our Machine Learning CI/CD Pipeline
![](https://github.com/iamlost127/codeday-ml-ci-cd/blob/master/images/cicd.png)
