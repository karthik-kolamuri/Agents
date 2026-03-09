// Prisma seed script for Q&A pairs (90 samples).

const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient();

const qaPairs = [
  {
    category: "PROJECT_INFO",
    question: "What is the name of the project?",
    answer:
      "The project is called Sunrise Heights, a premium residential community located in the heart of the city.",
    language: "en",
    tags: ["project_name"]
  },
  {
    category: "PROJECT_INFO",
    question: "Where is the project located?",
    answer:
      "Sunrise Heights is located near the IT corridor in Whitefield, close to major schools, hospitals, and shopping centers.",
    language: "en",
    tags: ["location"]
  },
  {
    category: "PROJECT_INFO",
    question: "What is the total land area of the project?",
    answer:
      "The project is spread across approximately 5 acres of land, with multiple residential towers and landscaped open spaces.",
    language: "en",
    tags: ["land_area"]
  },
  {
    category: "PROJECT_INFO",
    question: "How many towers and floors are there?",
    answer:
      "There are 4 residential towers, each with 15 floors, designed to maximize light, ventilation, and privacy.",
    language: "en",
    tags: ["towers", "floors"]
  },
  {
    category: "PROJECT_INFO",
    question: "What types of apartments are available?",
    answer:
      "We offer 1 BHK, 2 BHK, and 3 BHK apartments with different carpet areas and layout options.",
    language: "en",
    tags: ["bhk_types"]
  },
  {
    category: "PROJECT_INFO",
    question: "What is the size of a typical 2 BHK flat?",
    answer:
      "A typical 2 BHK at Sunrise Heights ranges from about 950 to 1,100 square feet of super built-up area.",
    language: "en",
    tags: ["2bhk_size"]
  },
  {
    category: "PROJECT_INFO",
    question: "Is the project RERA approved?",
    answer:
      "Yes, the project is fully RERA registered and compliant with all regulatory norms. We can share the RERA number during the site visit or over WhatsApp.",
    language: "en",
    tags: ["rera"]
  },
  {
    category: "PROJECT_INFO",
    question: "Who is the developer of this project?",
    answer:
      "The project is developed by Eficens Realty, a reputed builder with multiple on-time delivered projects in the region.",
    language: "en",
    tags: ["developer"]
  },
  {
    category: "PROJECT_INFO",
    question: "What amenities are available in the project?",
    answer:
      "Amenities include a clubhouse, swimming pool, children’s play area, gym, indoor games room, jogging track, landscaped gardens, and 24x7 security.",
    language: "en",
    tags: ["amenities"]
  },
  {
    category: "PROJECT_INFO",
    question: "Is there a clubhouse in the project?",
    answer:
      "Yes, we have a fully equipped clubhouse with a gym, indoor games, multi-purpose hall, and seating areas for residents.",
    language: "en",
    tags: ["clubhouse"]
  },
  {
    category: "PROJECT_INFO",
    question: "Do you have a swimming pool?",
    answer:
      "Yes, the project includes a swimming pool with a separate kids’ pool as part of the common amenities.",
    language: "en",
    tags: ["swimming_pool"]
  },
  {
    category: "PROJECT_INFO",
    question: "Is there covered car parking?",
    answer:
      "Yes, we provide covered car parking for residents, and visitor parking is also available within the premises.",
    language: "en",
    tags: ["parking"]
  },
  {
    category: "PROJECT_INFO",
    question: "What security features does the project have?",
    answer:
      "The project has 24x7 security with CCTV surveillance in common areas, access-controlled entry, and trained security staff.",
    language: "en",
    tags: ["security"]
  },
  {
    category: "PROJECT_INFO",
    question: "What is the possession timeline for the project?",
    answer:
      "The expected possession date is within the next 12 to 18 months, depending on the specific tower and unit.",
    language: "en",
    tags: ["possession_timeline"]
  },
  {
    category: "PROJECT_INFO",
    question: "Is the project ready to move in?",
    answer:
      "Some towers are nearing completion while others are under construction. Based on your timeline, we can suggest the best available options during a site visit.",
    language: "en",
    tags: ["ready_to_move"]
  },
  {
    category: "PROJECT_INFO",
    question: "What schools and hospitals are nearby?",
    answer:
      "There are multiple reputed schools, colleges, and multi-speciality hospitals within a 5 to 10 kilometer radius of the project.",
    language: "en",
    tags: ["nearby_schools_hospitals"]
  },
  {
    category: "PROJECT_INFO",
    question: "Is public transport easily available from the project?",
    answer:
      "Yes, the project is well connected by city buses, cabs, and autos, and the nearest metro station is within a short drive.",
    language: "en",
    tags: ["public_transport"]
  },
  {
    category: "PROJECT_INFO",
    question: "Do you have any sample flat or model flat to view?",
    answer:
      "Yes, we have a fully furnished model flat available. We can schedule a site visit at your preferred time to show it to you.",
    language: "en",
    tags: ["sample_flat"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "How can I book a flat in this project?",
    answer:
      "You can book a flat by selecting your preferred unit, paying the booking amount, and completing the basic documentation. Our sales team will guide you through each step during the site visit or over a call.",
    language: "en",
    tags: ["booking", "process"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "What documents are required for booking?",
    answer:
      "Generally, you need a copy of your PAN card, Aadhaar card, recent photographs, and basic income or employment details. Exact requirements will be shared by our sales executive.",
    language: "en",
    tags: ["documents"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "What is the initial booking amount?",
    answer:
      "The initial booking amount typically ranges from 1 to 2 lakh rupees, depending on the unit type. The exact amount will be confirmed during the discussion.",
    language: "en",
    tags: ["booking_amount"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Is the booking amount refundable?",
    answer:
      "In most cases, the booking amount is adjustable against the total flat cost and may be partially refundable as per the booking terms. Our sales team will explain the specific refund policy before you proceed.",
    language: "en",
    tags: ["refund_policy"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Can I reserve a flat for a few days before paying the full booking amount?",
    answer:
      "In some cases, we can hold a unit for a short period, subject to availability and management approval. It is best to discuss this with our sales executive quickly as inventory moves fast.",
    language: "en",
    tags: ["reserve_flat"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "What is the full process after paying the booking amount?",
    answer:
      "After the booking amount is paid, we issue a booking receipt, block your unit, share all legal documents, assist with loan processing if needed, and then move to agreement signing.",
    language: "en",
    tags: ["post_booking_process"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "How long does the entire booking process take?",
    answer:
      "If your documents are ready, the basic booking can be completed in a day. Agreement and loan processing may take a few additional days depending on the bank.",
    language: "en",
    tags: ["booking_timeline"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Can I book a flat online without visiting the site?",
    answer:
      "Yes, we can share videos, brochures, and layout plans digitally, and you can complete the booking process online with digital payments and e-signing, if you are comfortable.",
    language: "en",
    tags: ["online_booking"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Will someone assist me personally during the booking?",
    answer:
      "Yes, a dedicated sales consultant will assist you throughout the process—from initial inquiry to booking, documentation, and handover stages.",
    language: "en",
    tags: ["sales_assistance"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Can I change my flat after booking if I see a better option?",
    answer:
      "Change of unit is sometimes possible, subject to availability and internal policies. Any price difference will be adjusted accordingly.",
    language: "en",
    tags: ["change_flat"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "How do I get the project brochure and floor plans?",
    answer:
      "We can send you the brochure and detailed floor plans over WhatsApp, email, or SMS, and also show them during the site visit.",
    language: "en",
    tags: ["brochure", "floor_plans"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Can I include my spouse or family member as a co-applicant?",
    answer:
      "Yes, you can add a co-applicant or joint owner, which can also help in loan eligibility. Our team and the bank will guide you on the documentation.",
    language: "en",
    tags: ["co_applicant"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "What happens if my home loan is not approved?",
    answer:
      "If your loan is not approved, we will try alternate bank options. The exact booking and refund policy will be explained to you clearly before you pay.",
    language: "en",
    tags: ["loan_not_approved"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "After booking, when will the sale agreement be done?",
    answer:
      "The sale agreement is usually executed within a few weeks of booking, once the initial payment schedule and loan approvals are in place.",
    language: "en",
    tags: ["sale_agreement"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Who will coordinate with the bank for my loan during booking?",
    answer:
      "Our in-house loan coordination team will help you connect with our partner banks, submit documents, and track the approval process.",
    language: "en",
    tags: ["bank_coordination"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Can I visit the legal office or see all approvals before booking?",
    answer:
      "Yes, we can share a soft copy of approvals and, if needed, arrange a legal consultation so you feel fully confident before booking.",
    language: "en",
    tags: ["legal_approvals"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Is there any pre-booking offer or festival scheme running right now?",
    answer:
      "We do run time-bound offers or schemes. I can connect you to our sales team to share the latest offers applicable to your preferred unit type.",
    language: "en",
    tags: ["offers", "festival_scheme"]
  },
  {
    category: "BOOKING_PROCESS",
    question: "Can NRIs also book a flat in this project?",
    answer:
      "Yes, NRIs can book flats and we regularly handle NRI bookings. We will share the specific documentation and payment guidelines for NRI customers.",
    language: "en",
    tags: ["nri_booking"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Do you have any special payment plans?",
    answer:
      "Yes, we offer multiple payment schemes such as construction-linked plans, down payment plans, and sometimes subvention schemes in tie-up with banks.",
    language: "en",
    tags: ["payments", "schemes"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "What is the basic price of a 2 BHK?",
    answer:
      "The base price of a 2 BHK depends on the exact size and floor. As a ballpark, it starts from around ₹X lakh onwards. Our team will share a detailed price sheet for your preferred unit.",
    language: "en",
    tags: ["price", "2bhk"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "What is the all-inclusive cost of the flat?",
    answer:
      "The all-inclusive cost covers base price, floor rise, parking, clubhouse charges, GST, registration, and other applicable fees. We will provide a detailed breakup for complete transparency.",
    language: "en",
    tags: ["all_inclusive_cost"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "What is a construction-linked payment plan?",
    answer:
      "In a construction-linked plan, you pay a certain percentage at booking and the rest in stages linked to construction milestones, such as foundation, slab, brickwork, and finishing.",
    language: "en",
    tags: ["construction_linked"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Is there a down payment discount if I pay more upfront?",
    answer:
      "In many cases, we can offer a better price if you opt for a higher upfront payment or down payment plan. Our sales team can share the current offers.",
    language: "en",
    tags: ["down_payment_discount"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Do I need to pay the entire amount before possession?",
    answer:
      "For under-construction properties, payments are generally spread across milestones until possession. For ready-to-move units, the majority must be paid before registration.",
    language: "en",
    tags: ["payment_schedule"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Are there any hidden charges apart from the base price?",
    answer:
      "No, there are no hidden charges. We share a detailed cost sheet including taxes, registration, maintenance deposit, and other applicable charges upfront.",
    language: "en",
    tags: ["hidden_charges"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "What about maintenance charges?",
    answer:
      "There will be a one-time maintenance deposit and monthly maintenance charges for common area upkeep and amenities. The exact amount depends on the flat size and association decisions.",
    language: "en",
    tags: ["maintenance_charges"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Do you charge extra for car parking?",
    answer:
      "Yes, car parking is usually charged separately and depends on whether it is covered or open. The details will be listed in the cost sheet.",
    language: "en",
    tags: ["parking_charges"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Is GST included in the price?",
    answer:
      "GST is applicable as per government norms and will be clearly mentioned in the price breakup shared with you.",
    language: "en",
    tags: ["gst"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Can I negotiate the price of the flat?",
    answer:
      "Pricing depends on current inventory and demand. I can connect you with a senior sales manager who can discuss any available flexibility or offers.",
    language: "en",
    tags: ["negotiation"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Do you offer any no-cost EMI or special bank schemes?",
    answer:
      "From time to time, we partner with banks for special schemes like no pre-EMI or lower interest for an initial period. We can share details of the current schemes available.",
    language: "en",
    tags: ["no_cost_emi"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "What is the typical booking to possession payment ratio?",
    answer:
      "Typically, you pay about 10–20% as booking and agreement payments, and the rest is linked to construction progress and loan disbursements.",
    language: "en",
    tags: ["payment_ratio"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Are registration and stamp duty included in the quoted price?",
    answer:
      "Registration and stamp duty are usually extra and paid at the time of registration as per government rates. We will provide an estimate while sharing the cost sheet.",
    language: "en",
    tags: ["registration_stamp_duty"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Do you offer any discounts for full upfront payment?",
    answer:
      "In some cases, a preferential rate or discount may be possible for full or high upfront payment, subject to management approval.",
    language: "en",
    tags: ["upfront_discount"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Is there a penalty for delayed payments?",
    answer:
      "As per the agreement, delayed payments may attract interest or penalties. Our team will walk you through the terms before you sign.",
    language: "en",
    tags: ["delayed_payments"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Can I pay in parts before the bank loan is approved?",
    answer:
      "Yes, you can pay part of the amount from your own funds and the rest through a home loan, as long as it matches the agreed payment schedule.",
    language: "en",
    tags: ["part_payment"]
  },
  {
    category: "PAYMENT_SCHEMES",
    question: "Are there any early-bird or pre-launch pricing benefits?",
    answer:
      "Sometimes we have special pricing for early bookings or limited periods. I can ask our sales team to share any active early-bird offers with you.",
    language: "en",
    tags: ["early_bird"]
  },
  {
    category: "SITE_VISIT",
    question: "How can I schedule a site visit?",
    answer:
      "You can share your preferred date and time, and we will arrange a site visit with our sales team to give you a complete walkthrough of the project and sample flat.",
    language: "en",
    tags: ["site_visit", "scheduling"]
  },
  {
    category: "SITE_VISIT",
    question: "Are site visits available on weekends?",
    answer:
      "Yes, site visits are available on both weekdays and weekends. Weekend slots tend to fill up faster, so it’s good to book in advance.",
    language: "en",
    tags: ["weekend_visit"]
  },
  {
    category: "SITE_VISIT",
    question: "What are the visiting hours for the project?",
    answer:
      "Typically, site visits can be scheduled between 10 AM and 7 PM. We can try to accommodate slightly different timings on request.",
    language: "en",
    tags: ["visiting_hours"]
  },
  {
    category: "SITE_VISIT",
    question: "Do you provide pick-up and drop for the site visit?",
    answer:
      "Depending on your location and availability, we can sometimes arrange a cab or pick-up for serious buyers. Our team will confirm this when scheduling.",
    language: "en",
    tags: ["pickup_drop"]
  },
  {
    category: "SITE_VISIT",
    question: "Can I bring my family along for the site visit?",
    answer:
      "Absolutely, we encourage you to bring your family so everyone can see the project and give inputs.",
    language: "en",
    tags: ["family_visit"]
  },
  {
    category: "SITE_VISIT",
    question: "Will someone explain all details during the site visit?",
    answer:
      "Yes, a dedicated sales executive will walk you through the sample flat, amenities, pricing details, and answer all your questions on-site.",
    language: "en",
    tags: ["guided_tour"]
  },
  {
    category: "SITE_VISIT",
    question: "Can I see the actual flat where I will stay, not just the sample flat?",
    answer:
      "Where it is safe and allowed by site norms, we can show you the actual tower and approximate location of your flat. Access may be restricted for safety reasons in some under-construction areas.",
    language: "en",
    tags: ["actual_flat"]
  },
  {
    category: "SITE_VISIT",
    question: "Do I need to carry any documents for the site visit?",
    answer:
      "Documents are not mandatory for a basic visit. If you are planning to book on the same day, it’s helpful to carry your ID proofs and basic financial details.",
    language: "en",
    tags: ["documents_for_visit"]
  },
  {
    category: "SITE_VISIT",
    question: "How long does a typical site visit take?",
    answer:
      "A detailed site visit usually takes between 45 minutes to 1.5 hours, depending on how many options you want to see and discuss.",
    language: "en",
    tags: ["visit_duration"]
  },
  {
    category: "SITE_VISIT",
    question: "Can I take photos and videos during the site visit?",
    answer:
      "In most areas, you can take photos and short videos for personal reference. Our team will guide you if there are any restricted zones.",
    language: "en",
    tags: ["photos_videos"]
  },
  {
    category: "SITE_VISIT",
    question: "Will you show nearby facilities like schools and markets during the visit?",
    answer:
      "We can point out the nearby landmarks and, if feasible, plan a quick drive-by of key facilities around the project.",
    language: "en",
    tags: ["nearby_facilities"]
  },
  {
    category: "SITE_VISIT",
    question: "What if I want to reschedule my site visit?",
    answer:
      "You can reschedule easily by informing us before your slot, and we will arrange a new convenient time.",
    language: "en",
    tags: ["reschedule_visit"]
  },
  {
    category: "SITE_VISIT",
    question: "Can I have multiple site visits before making a decision?",
    answer:
      "Yes, you are welcome to visit more than once. We want you to be fully comfortable before taking a decision.",
    language: "en",
    tags: ["multiple_visits"]
  },
  {
    category: "SITE_VISIT",
    question: "Is there any fee for the site visit?",
    answer:
      "No, there is no charge for the site visit. It is completely free and without obligation.",
    language: "en",
    tags: ["visit_fee"]
  },
  {
    category: "SITE_VISIT",
    question: "Will a senior person be available during my visit if I have detailed questions?",
    answer:
      "We can arrange for a senior sales manager or technical person to be available, especially if you inform us about your specific queries in advance.",
    language: "en",
    tags: ["senior_person"]
  },
  {
    category: "SITE_VISIT",
    question: "Can I see the construction progress during the visit?",
    answer:
      "Yes, we will show you the current progress from safe viewing points and explain the construction timelines.",
    language: "en",
    tags: ["construction_progress"]
  },
  {
    category: "SITE_VISIT",
    question: "Will I get printed or digital materials during the site visit?",
    answer:
      "Yes, we can share brochures, floor plans, and cost sheets either in print at the site or digitally over WhatsApp and email.",
    language: "en",
    tags: ["materials"]
  },
  {
    category: "SITE_VISIT",
    question: "How do I confirm my site visit slot now?",
    answer:
      "You can share your preferred date, time, and contact details, and we will send you a confirmation SMS or WhatsApp message with the visit details.",
    language: "en",
    tags: ["confirm_slot"]
  },
  {
    category: "FINANCING",
    question: "Do you have tie-ups with banks for home loans?",
    answer:
      "Yes, we have tie-ups with multiple leading banks and housing finance companies to help you get competitive interest rates and faster approvals.",
    language: "en",
    tags: ["financing", "home_loan"]
  },
  {
    category: "FINANCING",
    question: "What is the maximum home loan I can get?",
    answer:
      "Your loan eligibility depends on your income, existing liabilities, credit score, and age. Our loan partners can quickly assess your eligibility once you share basic details.",
    language: "en",
    tags: ["loan_eligibility"]
  },
  {
    category: "FINANCING",
    question: "What is the current rate of interest on home loans?",
    answer:
      "Interest rates keep changing based on market conditions and the bank. Our loan team will share the latest rates from our partner banks when you inquire.",
    language: "en",
    tags: ["interest_rates"]
  },
  {
    category: "FINANCING",
    question: "Can you help me with the home loan documentation?",
    answer:
      "Yes, our in-house loan coordinators will guide you on the list of documents required and help submit them to the bank for processing.",
    language: "en",
    tags: ["loan_documentation"]
  },
  {
    category: "FINANCING",
    question: "How much down payment do I need to make?",
    answer:
      "Typically, banks finance up to 75–90% of the property cost, and you need to arrange the balance as down payment. The exact amount depends on bank norms and your profile.",
    language: "en",
    tags: ["down_payment"]
  },
  {
    category: "FINANCING",
    question: "I already have a pre-approved home loan. Can I use it here?",
    answer:
      "Yes, you can use your pre-approved loan for this project, subject to the bank’s property evaluation and documentation.",
    language: "en",
    tags: ["pre_approved_loan"]
  },
  {
    category: "FINANCING",
    question: "Do you support government subsidy schemes like PMAY if applicable?",
    answer:
      "If the project and your profile meet the government’s eligibility criteria, our loan partners can help you apply for available subsidy schemes.",
    language: "en",
    tags: ["subsidy"]
  },
  {
    category: "FINANCING",
    question: "What if my credit score is low?",
    answer:
      "A low credit score can affect loan eligibility, but our loan partners can still explore options or suggest ways to improve your profile before applying.",
    language: "en",
    tags: ["low_credit_score"]
  },
  {
    category: "FINANCING",
    question: "Can I take a joint loan with my spouse or parents?",
    answer:
      "Yes, joint loans with close family members are common and can increase your loan eligibility. The bank will advise you on the best structure.",
    language: "en",
    tags: ["joint_loan"]
  },
  {
    category: "FINANCING",
    question: "How long does it take to get a home loan sanctioned?",
    answer:
      "With complete documents, loan sanction can take anywhere from a few days to about two weeks, depending on the bank and your profile.",
    language: "en",
    tags: ["loan_sanction_time"]
  },
  {
    category: "FINANCING",
    question: "Is there any processing fee for the home loan?",
    answer:
      "Most banks charge a processing fee, usually a small percentage of the loan amount. Our loan partners will share the exact fee details.",
    language: "en",
    tags: ["processing_fee"]
  },
  {
    category: "FINANCING",
    question: "Can I transfer my existing home loan from another bank to this project?",
    answer:
      "You can explore balance transfer options with banks that have tie-ups with us, subject to their policies and your existing loan terms.",
    language: "en",
    tags: ["balance_transfer"]
  },
  {
    category: "FINANCING",
    question: "What if my loan is partially sanctioned and not for the full amount I want?",
    answer:
      "In that case, we can look at alternate banks or adjust the payment structure. Our team will work with you to find a practical solution.",
    language: "en",
    tags: ["partial_sanction"]
  },
  {
    category: "FINANCING",
    question: "Are there any pre-EMI schemes where I pay less in the beginning?",
    answer:
      "At times, developers and banks offer pre-EMI or subvention schemes where your EMI starts later. If such a scheme is active, we will explain the details during discussion.",
    language: "en",
    tags: ["pre_emi"]
  },
  {
    category: "FINANCING",
    question: "Will you help me compare offers from different banks?",
    answer:
      "Yes, we can connect you to multiple loan partners so you can compare interest rates, processing fees, and terms before deciding.",
    language: "en",
    tags: ["compare_offers"]
  },
  {
    category: "FINANCING",
    question: "Can I foreclose or prepay my home loan without penalty?",
    answer:
      "Many banks allow part-prepayment or foreclosure with minimal or no penalty, especially for floating rate loans. Your chosen bank will clarify their exact policy.",
    language: "en",
    tags: ["foreclosure"]
  },
  {
    category: "FINANCING",
    question: "Do I get tax benefits on home loan EMI?",
    answer:
      "Yes, home loans generally offer tax benefits on both principal and interest components under the Income Tax Act. Your CA or tax advisor can guide you on the exact sections and limits.",
    language: "en",
    tags: ["tax_benefits"]
  },
  {
    category: "FINANCING",
    question: "I am self-employed. Can I still get a home loan?",
    answer:
      "Yes, self-employed professionals and business owners are eligible for home loans. You will need to share income proofs like IT returns, bank statements, and business documents with the bank.",
    language: "en",
    tags: ["self_employed"]
  }
];

async function main() {
  for (const qa of qaPairs) {
    await prisma.qAPair.upsert({
      where: { question: qa.question },
      update: {},
      create: qa
    });
  }
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });

