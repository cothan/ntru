CC = clang
CFLAGS = -O3 -fomit-frame-pointer -mtune=native -g3 -mcpu=cortex-a53 -fPIC -fPIE -pie -flax-vector-conversions
LDFLAGS = -lkeccak -lpapi

SRC = fips202.c \
      kem.c \
      owcpa.c \
      pack3.c \
      packq.c \
      poly.c \
      poly_r2_inv.c \
      sample.c \
	  asimd_asmgen/intrin_c/intrin_poly_mod_3_Phi_n_formatted.c \
	  asimd_asmgen/intrin_c/intrin_poly_mod_q_Phi_n_formatted.c \
	  asimd_asmgen/intrin_c/intrin_poly_rq_to_s3_formatted.c \
	  asimd_asmgen/intrin_c/intrin_sample_iid_formated.c \
	  asimd_asmgen/rq_mul/intrin_c/intrin_K2_K2_64x44_formatted.c \
	  asimd_asmgen/rq_mul/intrin_c/intrin_poly_rq_mul_formatted.c \
	  poly_lift.c \
	  poly_s3_inv.c \
      verify.c

HDR = kem.h \
      owcpa.h \
      params.h \
      poly.h \
      sample.h \
      verify.h

SRC_URAND = $(SRC) randombytes.c
HDR_URAND = $(HDR) randombytes.h

SRC_KAT = $(SRC) rng.c PQCgenKAT_kem.c
HDR_KAT = $(HDR) rng.h api.h


all: test/test_polymul \
     test/test_ntru \
     test/test_pack \
     test/ram \
     test/speed \
     test/encap \
     test/decap \
     test/keypair \
     test/speed_r2_inv

test/test_polymul: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/test_polymul.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/test_polymul.c cpucycles.c

test/test_ntru: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/test_ntru.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/test_ntru.c cpucycles.c

test/test_pack: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/test_pack.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/test_pack.c cpucycles.c

test/ram: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/ram.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/ram.c

test/speed: $(SRC_URAND) $(OBJS) $(HDR_URAND) cpucycles.h cpucycles.c test/speed.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) cpucycles.c test/speed.c $(LDFLAGS)

test/speed_r2_inv: $(SRC_URAND) $(OBJS) $(HDR_URAND) cpucycles.h cpucycles.c test/speed_r2_inv.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) cpucycles.c test/speed_r2_inv.c

test/encap: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/encap.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/encap.c

test/decap: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/decap.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/decap.c

test/keypair: $(SRC_URAND) $(OBJS) $(HDR_URAND) test/keypair.c
	$(CC) $(CFLAGS) -o $@ $(SRC_URAND) $(OBJS) test/keypair.c

PQCgenKAT_kem: $(SRC_KAT) $(HDR_KAT) $(OBJS) 
	$(CC) $(CFLAGS) -o $@ $(SRC_KAT) $(OBJS) -lcrypto $(LDFLAGS)

.PHONY: clean test

# Useful for the .s files;
.DELETE_ON_ERROR:

test:
	./test/test_polymul
	./test/test_ntru
	./test/test_pack
	./test/speed
	./test/ram
	./test/speed_r2_inv

clean:
	-find . -name '*.pyc' -delete
	-find . -name '__pycache__' -delete
	-$(RM) *.o
	-$(RM) *.s
	-$(RM) -r test/test_polymul
	-$(RM) -r test/test_ntru
	-$(RM) -r test/test_pack
	-$(RM) -r test/speed
	-$(RM) -r test/ram
	-$(RM) -r test/encap
	-$(RM) -r test/decap
	-$(RM) -r test/keypair
	-$(RM) -r test/speed_r2_inv
	-$(RM) PQCgenKAT_kem
	-$(RM) PQCkemKAT_*.req
	-$(RM) PQCkemKAT_*.rsp
