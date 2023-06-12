   /**
     * Setup
     * @param ctx context, String security
     * generate params
     */
    @Transaction(name = "Setup", intent = Transaction.TYPE.SUBMIT)
    public void Setup(final Context ctx, final String security) {
        ChaincodeStub stub = ctx.getStub();
        int securityInt = Integer.parseInt(security);

        //生成p，q需要满足大质数性质
        BigInteger p = BigInteger.probablePrime(2 * securityInt, new Random());
        BigInteger q = p.multiply(BigInteger.valueOf(2)).add(BigInteger.valueOf(1));

        //生成g，h只需要在1到q-1的范围内 
        Random random = new Random();
        BigInteger g = new BigInteger(String.valueOf(random.nextInt(q.intValue()) + 1)) ;
        BigInteger s = new BigInteger(String.valueOf(random.nextInt(q.intValue()) + 1)) ;

        //根据相应关系计算h
        BigInteger h = g.modPow(s,q);


        //put参数
        stub.putStringState("q", String.valueOf(p));
        stub.putStringState("g", String.valueOf(g));
        stub.putStringState("h", String.valueOf(h));

    }


    /**
     * Commitment
     * @param ctx context, xStr String, org String, customer String
     * encrypton information
     */
    @Transaction(name = "commit", intent = Transaction.TYPE.SUBMIT)
    public void commit(final Context ctx, final String xStr, final String org, final String customer) throws IOException {
        ChaincodeStub stub = ctx.getStub();
        Random random = new Random();
        //获取已经put的所有参数
        BigInteger q = new BigInteger(stub.getStringState("q"));
        BigInteger g = new BigInteger(stub.getStringState("g"));
        BigInteger h = new BigInteger(stub.getStringState("h"));
        BigInteger x = new BigInteger(xStr);

        String r_ = stub.getStringState(org);
        BigInteger r = null;
        if (r_.isEmpty()) {//判断r是否存在
             r = new BigInteger(String.valueOf(random.nextInt(q.intValue()) + 1));  //若不存在，则生成r
             stub.putStringState(org, String.valueOf(r));//put r
        }else{
             r = new BigInteger(r_);//从org获取r
        }
        
        BigInteger c = g.modPow(x,q).multiply(h.modPow(r,q)).mod(q);//计算c，即加密数据

        stub.putStringState(org+customer, String.valueOf(c));//put c
       
    }

  @Transaction(name = "Open", intent = Transaction.TYPE.EVALUATE)
    public String Open(final Context ctx, final String cStr,final String xStr,final String rStr) {
        ChaincodeStub stub = ctx.getStub();

        //获取参数
        BigInteger q = new BigInteger(stub.getStringState("q"));
        BigInteger g = new BigInteger(stub.getStringState("g"));
        BigInteger h = new BigInteger(stub.getStringState("h"));
        //x为加密信息，r为random，c是加密之后的信息
        BigInteger x = new BigInteger(xStr);
        BigInteger r = new BigInteger(rStr);
        BigInteger c = new BigInteger(cStr);

        //计算结果
        BigInteger mod = g.modPow(x, q).multiply(h.modPow(r, q)).mod(q);

        //验证判断
        if (c.equals(mod)){
            return "True";
        }else {
            return "False";
        }
    }

    @Transaction(name = "GetValue", intent = Transaction.TYPE.EVALUATE)
    public String GetValue(final Context ctx,final String key){
        ChaincodeStub stub = ctx.getStub();
        String value = stub.getStringState(key);
         // key not existing
        if (value.isEmpty()) {
            String errorMessage = "No key found";
            System.out.println("No key found");
            throw new ChaincodeException(errorMessage);
        }
        return value;
    }

     /**
     * Verify Amount
     * @param ctx Context
     * @param orgs Array - Elements are String Objects 
     * @param cid String - Customer's ID in String format
     * @param input BigInteger - Customer's real loan amount to verify
     * @return true or false
     */
      @Transaction(name = "verify", intent = Transaction.TYPE.EVALUATE)
    public String verify(final Context ctx, final String cid, final String input)throws IOException {
        ChaincodeStub stub = ctx.getStub();

        // get parameters
        BigInteger q = new BigInteger(stub.getStringState("q"));
        BigInteger g = new BigInteger(stub.getStringState("g"));
        BigInteger h = new BigInteger(stub.getStringState("h"));

        
        String[] orgs = {"org00001", "org00002"};

        // concat keys and get values
        BigInteger sum = new BigInteger("1");
        BigInteger r = new BigInteger("0");
        BigInteger verifiedInput;
        for (int i = 0; i < orgs.length; i++) {
            String key = orgs[i] + cid;
            String keyValue = stub.getStringState(key);
            String rValue = stub.getStringState(orgs[i]);
            
            //judge existence
            if(keyValue.isEmpty()){
                return key + " not exist";
            }

             if(rValue.isEmpty()){
                return orgs[i] + " not exist";
            }

            sum = sum.multiply(new BigInteger(keyValue));
            r = r.add(new BigInteger(rValue));
        }


        BigInteger result= sum.mod(q);
        
        // create encrypted value of the input which is a real amount of a customer's loan
        verifiedInput = g.modPow(new BigInteger(input), q).multiply(h.modPow(r, q)).mod(q);

        // print result
        if (verifiedInput.compareTo(result) != 0) {
            return "result " + String.valueOf(result) + "r " + String.valueOf(r);
        } else {
            return "True";
        }
    }
