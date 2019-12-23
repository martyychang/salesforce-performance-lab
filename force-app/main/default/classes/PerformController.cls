@RestResource(urlMapping='/perform')
global class PerformController {

    global static final Integer DEFAULT_NUMBER_OF_RUNS = 10;

    global static final String NUMBER_OF_RUNS_PARAM = 'numberofruns';

    global static final String TEST_NAME_PARAM = 'testname';

    @HttpGet
    global static PerformResult perform() {

        // Get a handle on the request
        RestRequest req = RestContext.request;
        
        // Determine how many times to run the test
        Integer numberOfRuns = req.params.containsKey(NUMBER_OF_RUNS_PARAM)
                ? Integer.valueOf(req.params.get(NUMBER_OF_RUNS_PARAM))
                : DEFAULT_NUMBER_OF_RUNS;

        // Initialize the result
        PerformResult result = new PerformResult(
            req.params.get(TEST_NAME_PARAM),
            numberOfRuns
        );

        // Run the test
        for (Integer i = 0; i < numberOfRuns; i++) {

            // Determine the Apex class to instantiate
            Type testType = Type.forName(req.params.get(TEST_NAME_PARAM));

            // Add the sample from a new run to the list in the result
            result.samples.add(
                ((Performable)testType.newInstance()).execute(req.params)
            );
        }

        return result;
    }

    global class PerformResult {
        global String name;
        global Integer numberOfRuns;
        global List<PerformSample> samples;

        public PerformResult(String name, Integer numberOfRuns) {
            this.name = name;
            this.numberOfRuns = numberOfRuns;
            this.samples = new List<PerformSample>();
        }
    }

    global class PerformSample {
        global Long measuredDuration;
        global Long runDate;

        global PerformSample(Long measuredDuration, Datetime runDatetime) {
            this.measuredDuration = measuredDuration;
            this.runDate = runDatetime.getTime();
        }
    }
}